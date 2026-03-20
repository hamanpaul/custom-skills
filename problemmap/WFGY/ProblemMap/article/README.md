# RAG Problem Map – Article Index (MVP)

single place to find every Discussion article. each line links out. this page is the canonical index.

*Last updated: 2025-08-22*

---

## Day 1–16 index

* **Day 1: PDFs poison your embedding space** *(Problem Map No.1, No.5)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/25](https://github.com/onestardao/WFGY/discussions/25)

* **Day 2: OCR noise and phantom tokens** *(No.1, No.11)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/26](https://github.com/onestardao/WFGY/discussions/26)

* **Day 3: Multi-version PDFs cause timeline confusion** *(No.2, No.6)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/27](https://github.com/onestardao/WFGY/discussions/27)

* **Day 4: Bad chunking ruins retrieval** *(No.5, No.14)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/28](https://github.com/onestardao/WFGY/discussions/28)

* **Day 5: Semantic ≠ Embedding** *(No.5)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/29](https://github.com/onestardao/WFGY/discussions/29)

* **Day 6: Vector anisotropy and collapse** *(No.5, No.6)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/30](https://github.com/onestardao/WFGY/discussions/30)

* **Day 7: Empty vectors and FAISS pitfalls** *(No.8)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/32](https://github.com/onestardao/WFGY/discussions/32)

* **Day 8: Retriever looks fine, answers still collapse** *(No.6)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/33](https://github.com/onestardao/WFGY/discussions/33)

* **Day 9: Over-reliance on reranker** *(No.5, No.6)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/34](https://github.com/onestardao/WFGY/discussions/34)

* **Day 10: Memory breaks across sessions** *(No.7)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/35](https://github.com/onestardao/WFGY/discussions/35)

* **Day 11: Logic collapse and recovery** *(No.6)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/36](https://github.com/onestardao/WFGY/discussions/36)

* **Day 12: Bootstrap ordering mistake** *(No.14)*
  Discussion  → [https://github.com/onestardao/WFGY/discussions/37](https://github.com/onestardao/WFGY/discussions/37)

* **Day 13: Multi-agent chaos** *(No.13)*
  Discussion →  [https://github.com/onestardao/WFGY/discussions/38](https://github.com/onestardao/WFGY/discussions/38)

* **Day 14: Symbolic collapse** *(No.11)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/39](https://github.com/onestardao/WFGY/discussions/39)

* **Day 15: Creative freeze** *(No.10)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/40](https://github.com/onestardao/WFGY/discussions/40)

* **Day 16: Deployment deadlock** *(No.15)*
  Discussion → [https://github.com/onestardao/WFGY/discussions/41](https://github.com/onestardao/WFGY/discussions/41)

---

## what each article should include

keep it short, testable, and reproducible. suggested skeleton:

1. **Symptoms**
   one paragraph with concrete failure signs that an engineer can verify.

2. **Root cause in the embedding space**
   name the failure mode and how it maps to **Problem Map No.X**.

3. **10-minute diagnosis**
   two to four checks. keep at least one copy-paste code snippet or CLI step.

4. **Minimal fix**
   steps that can be applied the same day. avoid vendor lock. note any defaults.

5. **Acceptance test**
   clear pass condition. one line people can add to logs for auditability.

6. **Reproduce a semantic firewall overlay in about a minute**
   remind that there is no infra change. one file and one prompt. show the short prompt.

7. **Mapping**
   list all matching Problem Map items using **No.** numbering. example
   `No.1 hallucination and chunk drift, No.5 semantic ≠ embedding`.

---

## footer snippet to paste in every Discussion

```
This article is part of the Problem Map series (Day 1–16).
Series index: https://github.com/onestardao/WFGY/blob/main/ProblemMap/article/README.md
Problem Map overview: https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md
```

---

## status tracker

* Day 1 posted
* Day 2 draft
* Day 3 draft
* Day 4 draft
* Day 5 draft
* Day 6 draft
* Day 7 draft
* Day 8 draft
* Day 9 draft
* Day 10 draft
* Day 11 draft
* Day 12 draft
* Day 13 draft
* Day 14 draft
* Day 15 draft
* Day 16 draft

---

## notes

* use **No.** when referencing Problem Map numbers
* keep article links pointed to GitHub Discussions to encourage comments
* once a week, update this index with the new discussion urls
