#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["chromadb==1.5.9"]
# ///
# Course copy of the author's ~/.local/bin/doc-search. Docling and poppler
# (pdfimages, pdftoppm) are external tools: `uv tool install docling`.
"""Index local documents and print short, sourced excerpts.

Chunks follow the document's sections (Docling HybridChunker) and carry
pages and headings. Search fuses dense (Chroma), keyword (SQLite FTS5,
BM25) and optional regex ranks. Checked answers can be cached as notes.
"""

import argparse
import datetime
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path.home() / ".local/share/doc-index"
MD_ROOT = ROOT / "markdown"
CHROMA_PATH = ROOT / "chroma"
DB_PATH = ROOT / "chunks.db"
DOCLING = Path(shutil.which("docling") or Path.home() / ".local/bin/docling")
# all-MiniLM-L6-v2, Chroma's default embedder, reads at most 256 tokens.
MAX_TOKENS = 256
CHUNKER = f"hybrid-{MAX_TOKENS}"
TXT_CHARS = 1000
MAX_PRINT_CHARS = 12000
RRF_K = 60
OFFICE = {".pdf", ".docx", ".pptx", ".ppt", ".doc", ".html", ".md"}
TEXT = {".txt"}


def source_id(path: Path) -> str:
    return hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]


def cache_dir(path: Path) -> Path:
    return MD_ROOT / source_id(path)


def page_span(pages: list[int]) -> str:
    if not pages:
        return ""
    lo, hi = min(pages), max(pages)
    return str(lo) if lo == hi else f"{lo}-{hi}"


def split_plain(text: str) -> list[dict]:
    records, buf = [], ""
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if buf and len(buf) + len(para) > TXT_CHARS:
            records.append(buf)
            buf = ""
        buf = f"{buf}\n\n{para}".strip()
    if buf:
        records.append(buf)
    return [{"pages": "", "section": "", "text": t, "body": t} for t in records]


def run_docling(path: Path, out_dir: Path) -> tuple[str, list[dict]]:
    if not DOCLING.is_file():
        raise SystemExit("Docling not found: install with `uv tool install docling`")
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.iterdir():
        if old.is_file():
            old.unlink()
    subprocess.run(
        [
            str(DOCLING),
            "convert",
            str(path),
            "--to",
            "md",
            "--to",
            "chunks",
            "--chunks-type",
            "hybrid",
            "--chunks-max-tokens",
            str(MAX_TOKENS),
            "--output",
            str(out_dir),
            "--image-export-mode",
            "placeholder",
        ],
        check=True,
    )
    mds = sorted(out_dir.glob("*.md"))
    jsonl = sorted(out_dir.glob("*.chunks.jsonl"))
    if not mds or not jsonl:
        raise SystemExit(f"Docling wrote no Markdown or chunks for {path}")
    records = []
    for line in jsonl[0].read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        body = (item.get("raw_text") or item.get("text") or "").strip()
        if not body:
            continue
        records.append(
            {
                "pages": page_span(item.get("page_numbers") or []),
                "section": " > ".join(item.get("headings") or []),
                "text": item.get("text") or body,
                "body": body,
            }
        )
    return mds[0].read_text(encoding="utf-8"), records


def convert(path: Path) -> list[dict]:
    """Return chunk records; reuse the cache while mtime and chunker match."""
    cdir = cache_dir(path)
    dest, chunks_path, meta_path = (
        cdir / "text.md",
        cdir / "chunks.jsonl",
        cdir / "source.json",
    )
    mtime = path.stat().st_mtime
    if dest.is_file() and chunks_path.is_file() and meta_path.is_file():
        recorded = json.loads(meta_path.read_text(encoding="utf-8"))
        if recorded.get("mtime") == mtime and recorded.get("chunker") == CHUNKER:
            lines = chunks_path.read_text(encoding="utf-8").splitlines()
            return [json.loads(x) for x in lines if x.strip()]
    cdir.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in TEXT:
        text = path.read_text(encoding="utf-8")
        records = split_plain(text)
    else:
        text, records = run_docling(path, cdir / "docling")
    dest.write_text(text, encoding="utf-8")
    chunks_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
        encoding="utf-8",
    )
    meta_path.write_text(
        json.dumps(
            {"source": str(path.resolve()), "mtime": mtime, "chunker": CHUNKER},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return records


def chroma(name: str = "documents"):
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    if name == "notes":
        return client.get_or_create_collection(
            name="notes", configuration={"hnsw": {"space": "cosine"}}
        )
    return client.get_or_create_collection(name=name)


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS chunks(
          id TEXT PRIMARY KEY, source TEXT, chunk INTEGER,
          pages TEXT, section TEXT, body TEXT);
        CREATE INDEX IF NOT EXISTS chunks_source ON chunks(source, chunk);
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
          text, section, id UNINDEXED, source UNINDEXED,
          tokenize='porter unicode61');
        """
    )
    return con


def drop_stale_notes(source: str, mtime: float) -> None:
    notes = chroma("notes")
    got = notes.get(where={"source": source})
    stale = [i for i, m in zip(got["ids"], got["metadatas"]) if m.get("mtime") != mtime]
    if stale:
        notes.delete(ids=stale)
        print(f"Removed {len(stale)} note(s) written for an older version")


def index_file(path: Path) -> None:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"Not a file: {path}")
    if path.suffix.lower() not in OFFICE | TEXT:
        raise SystemExit(f"Unsupported type: {path.suffix}")
    records = convert(path)
    if not records:
        raise SystemExit(f"No text extracted from {path}")
    source = str(path)
    store = chroma()
    store.delete(where={"source": source})
    con = db()
    ids = []
    with con:
        con.execute("DELETE FROM chunks WHERE source = ?", (source,))
        con.execute("DELETE FROM chunks_fts WHERE source = ?", (source,))
        for index, rec in enumerate(records):
            cid = hashlib.sha256(f"{source}:{index}".encode()).hexdigest()
            ids.append(cid)
            con.execute(
                "INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?)",
                (cid, source, index, rec["pages"], rec["section"], rec["body"]),
            )
            con.execute(
                "INSERT INTO chunks_fts VALUES (?, ?, ?, ?)",
                (rec["text"], rec["section"], cid, source),
            )
    batch = 64
    for start in range(0, len(ids), batch):
        part = records[start : start + batch]
        store.upsert(
            ids=ids[start : start + batch],
            documents=[r["text"] for r in part],
            metadatas=[
                {
                    "source": source,
                    "chunk": start + k,
                    "pages": r["pages"],
                    "section": r["section"],
                }
                for k, r in enumerate(part)
            ],
        )
    drop_stale_notes(source, path.stat().st_mtime)
    with_section = sum(1 for r in records if r["section"])
    print(
        f"Indexed {len(ids)} chunks ({with_section} with a section heading) "
        f"from {source}"
    )


def check_notes(query: str, source: str | None, threshold: float) -> bool:
    notes = chroma("notes")
    if not query.strip() or notes.count() == 0:
        return False
    kwargs = {"query_texts": [query], "n_results": 1}
    if source:
        kwargs["where"] = {"source": source}
    res = notes.query(**kwargs)
    if not res["ids"][0]:
        return False
    sim = 1 - res["distances"][0][0]
    if sim < threshold:
        return False
    meta = res["metadatas"][0][0]
    p = meta.get("pages") or ""
    pages = (f", pp. {p}" if "-" in p else f", p. {p}") if p else ""
    print(
        f"CACHED NOTE {res['ids'][0][0]} (similarity {sim:.2f}, "
        f"written {meta.get('date')}{pages})"
    )
    print(f"SOURCE: {meta.get('source')}")
    print(f"QUESTION: {res['documents'][0][0]}")
    print(f"ANSWER: {meta.get('answer')}")
    print("[cached answer; pass --no-notes for fresh excerpts]")
    return True


def dense_ranks(query: str, source: str | None, n: int) -> dict[str, int]:
    store = chroma()
    if not query.strip() or store.count() == 0:
        return {}
    kwargs = {"query_texts": [query], "n_results": min(n, store.count())}
    if source:
        kwargs["where"] = {"source": source}
    ids = store.query(**kwargs)["ids"][0]
    return {cid: r for r, cid in enumerate(ids, 1)}


def lexical_ranks(
    con: sqlite3.Connection, query: str, source: str | None, n: int
) -> dict[str, int]:
    tokens = re.findall(r"\w+", query)
    if not tokens:
        return {}
    match = " OR ".join(f'"{t}"' for t in tokens)
    sql = "SELECT id FROM chunks_fts WHERE chunks_fts MATCH ?"
    params: list = [match]
    if source:
        sql += " AND source = ?"
        params.append(source)
    sql += " ORDER BY bm25(chunks_fts) LIMIT ?"
    params.append(n)
    rows = con.execute(sql, params).fetchall()
    return {cid: r for r, (cid,) in enumerate(rows, 1)}


def regex_hits(
    con: sqlite3.Connection, patterns: list[str], ignore_case: bool, source: str | None
) -> dict[str, int]:
    flags = re.IGNORECASE if ignore_case else 0
    compiled = []
    for p in patterns:
        try:
            compiled.append(re.compile(p, flags))
        except re.error as exc:
            raise SystemExit(f"Bad --regex {p!r}: {exc}") from exc
    sql = "SELECT id, section, body FROM chunks"
    params: tuple = ()
    if source:
        sql += " WHERE source = ?"
        params = (source,)
    hits = {}
    for cid, section, body in con.execute(sql, params):
        count = sum(len(rx.findall(f"{section}\n{body}")) for rx in compiled)
        if count:
            hits[cid] = count
    return hits


def search(args: argparse.Namespace) -> None:
    query = args.query or ""
    if not query.strip() and not args.regex:
        raise SystemExit("Give a query, a --regex, or both")
    source = str(Path(args.source).expanduser().resolve()) if args.source else None
    if not args.no_notes and check_notes(query, source, args.note_threshold):
        return
    con = db()
    pool = max(10 * args.limit, 50)
    dense = dense_ranks(query, source, pool)
    lexical = lexical_ranks(con, query, source, pool)
    counts = regex_hits(con, args.regex, args.ignore_case, source) if args.regex else {}
    regex = {
        cid: r for r, cid in enumerate(sorted(counts, key=counts.get, reverse=True), 1)
    }
    scores: dict[str, float] = {}
    for ranks, weight in (
        (dense, args.w_dense),
        (lexical, args.w_lexical),
        (regex, args.w_regex),
    ):
        for cid, rank in ranks.items():
            scores[cid] = scores.get(cid, 0.0) + weight / (RRF_K + rank)
    top = sorted(scores, key=scores.get, reverse=True)[: max(1, args.limit)]
    if not top:
        print("No excerpts.")
        return
    used = 0
    seen_sections = set()
    for cid in top:
        row = con.execute(
            "SELECT source, chunk, pages, section, body FROM chunks WHERE id = ?",
            (cid,),
        ).fetchone()
        if row is None:
            continue
        src, chunk, pages, section, body = row
        tags = []
        if cid in dense:
            tags.append(f"dense#{dense[cid]}")
        if cid in lexical:
            tags.append(f"lexical#{lexical[cid]}")
        if cid in counts:
            tags.append(f"regex:{counts[cid]}")
        if args.whole_section and section:
            if (src, section) in seen_sections:
                continue
            seen_sections.add((src, section))
            parts = con.execute(
                "SELECT chunk, pages, body FROM chunks "
                "WHERE source = ? AND section = ? ORDER BY chunk",
                (src, section),
            ).fetchall()
            chunk = page_span([parts[0][0], parts[-1][0]])
            spans = [int(p) for _, ps, _ in parts for p in ps.split("-") if p]
            pages = page_span(spans)
            body = "\n\n".join(b for _, _, b in parts)
        piece = body[: MAX_PRINT_CHARS - used]
        used += len(piece)
        print(f"\nSOURCE: {src}")
        if pages:
            print(f"PAGES: p. {pages}")
        if section:
            print(f"SECTION: {section}")
        print(f"CHUNK: {chunk}")
        print(f"RANKS: {' '.join(tags)}")
        print(piece)
        print("---")
        if used >= MAX_PRINT_CHARS:
            print("\n[stopped at about 3000 tokens]")
            break


def note(args: argparse.Namespace) -> None:
    notes = chroma("notes")
    if args.note_cmd == "add":
        path = Path(args.source).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"Not a file: {path}")
        nid = hashlib.sha256(f"{path}:{args.question}".encode()).hexdigest()[:16]
        notes.upsert(
            ids=[nid],
            documents=[args.question],
            metadatas=[
                {
                    "source": str(path),
                    "answer": args.answer,
                    "pages": args.pages or "",
                    "mtime": path.stat().st_mtime,
                    "date": datetime.date.today().isoformat(),
                }
            ],
        )
        print(f"Saved note {nid}")
    elif args.note_cmd == "list":
        kwargs = {}
        if args.source:
            kwargs["where"] = {"source": str(Path(args.source).expanduser().resolve())}
        got = notes.get(**kwargs)
        if not got["ids"]:
            print("No notes.")
        for nid, q, m in zip(got["ids"], got["documents"], got["metadatas"]):
            print(f"{nid}  {m.get('date')}  {m.get('source')}")
            print(f"  Q: {q}")
            print(f"  A: {m.get('answer')}")
    else:
        if not notes.get(ids=[args.id])["ids"]:
            raise SystemExit(f"No note {args.id}")
        notes.delete(ids=[args.id])
        print(f"Deleted note {args.id}")


CAPTION = re.compile(r"^\s*(?:Figure|Fig\.)\s*(\d+)[.:]?\s*(.*)$", re.MULTILINE)


def figures(args: argparse.Namespace) -> None:
    """Extract embedded images and render caption pages for one PDF."""
    path = Path(args.file).expanduser().resolve()
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise SystemExit(f"Not a PDF file: {path}")
    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    out = Path(args.out).expanduser().resolve() / slug / "figures"
    out.mkdir(parents=True, exist_ok=True)
    found: dict[int, dict] = {}
    for rec in convert(path):
        for m in CAPTION.finditer(rec["body"]):
            num = int(m.group(1))
            if num not in found and rec["pages"]:
                lo, _, hi = rec["pages"].partition("-")
                found[num] = {
                    "figure": num,
                    "caption": m.group(0).strip(),
                    "pages": list(range(int(lo), int(hi or lo) + 1)),
                }
    pages = sorted({p for f in found.values() for p in f["pages"]})
    if args.pages:
        pages = sorted(set(pages) | {int(p) for p in args.pages.split(",")})
    subprocess.run(["pdfimages", "-png", "-p", str(path), str(out / "raw")], check=True)
    for p in pages:
        subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-r",
                str(args.dpi),
                "-f",
                str(p),
                "-l",
                str(p),
                "-singlefile",
                str(path),
                str(out / f"p{p:02d}"),
            ],
            check=True,
        )
    raw = sorted(x.name for x in out.glob("raw-*.png"))
    for f in found.values():
        f["renders"] = [f"figures/p{p:02d}.png" for p in f["pages"]]
        f["raw_images"] = [
            f"figures/{n}" for n in raw if int(n.split("-")[1]) in f["pages"]
        ]
    index = out.parent / "figure-candidates.json"
    index.write_text(
        json.dumps(
            {"source": str(path), "dpi": args.dpi, "figures": list(found.values())},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"{len(found)} figure caption(s) on page(s) {pages or 'none'}")
    print(f"{len(raw)} embedded image(s), {len(pages)} page render(s) in {out}")
    print(f"Candidates: {index}")
    print("Look at each image before describing it; discard logos and icons.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search locally indexed documents")
    sub = parser.add_subparsers(dest="cmd", required=True)
    index_parser = sub.add_parser("index", help="Convert and index one file")
    index_parser.add_argument("file")
    sp = sub.add_parser("search", help="Return a few sourced excerpts")
    sp.add_argument("query", nargs="?", default="")
    sp.add_argument("--limit", type=int, default=5)
    sp.add_argument("--source", help="Restrict results to one file path")
    sp.add_argument(
        "--regex", action="append", default=[], help="Pattern to match (repeatable)"
    )
    sp.add_argument("-i", "--ignore-case", action="store_true", help="For --regex")
    sp.add_argument("--w-dense", type=float, default=1.0)
    sp.add_argument("--w-lexical", type=float, default=1.0)
    sp.add_argument("--w-regex", type=float, default=2.0)
    sp.add_argument(
        "--whole-section", action="store_true", help="Print each hit's full section"
    )
    sp.add_argument("--no-notes", action="store_true", help="Skip cached answers")
    sp.add_argument("--note-threshold", type=float, default=0.90)
    np_ = sub.add_parser("note", help="Cache checked answers")
    nsub = np_.add_subparsers(dest="note_cmd", required=True)
    add = nsub.add_parser("add")
    add.add_argument("--source", required=True)
    add.add_argument("--question", required=True)
    add.add_argument("--answer", required=True)
    add.add_argument("--pages")
    lst = nsub.add_parser("list")
    lst.add_argument("--source")
    dele = nsub.add_parser("delete")
    dele.add_argument("id")
    fp = sub.add_parser("figures", help="Extract images and render caption pages")
    fp.add_argument("file")
    fp.add_argument("--slug", help="Folder name (default: file stem)")
    fp.add_argument("--out", default=".firecrawl/extract", help="Extraction root")
    fp.add_argument("--dpi", type=int, default=200)
    fp.add_argument("--pages", help="Extra pages to render, e.g. 3,5")
    args = parser.parse_args()
    if args.cmd == "index":
        index_file(Path(args.file))
    elif args.cmd == "search":
        search(args)
    elif args.cmd == "figures":
        figures(args)
    else:
        note(args)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except KeyboardInterrupt:
        sys.exit(130)
