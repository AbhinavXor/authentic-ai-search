> ⚠️ The exact weighting formula is an internal implementation detail that continues to be tuned. The score is a **heuristic relative confidence indicator**, not a mathematical guarantee of correctness.

---

## 🏷️ Verification Levels

| Badge | Status Value | Meaning |
|---|---|---|
| ✅ **Verified** | `verified` | High agreement across multiple authoritative, reachable sources. |
| ⚠️ **Partially Verified** | `partially_verified` | Some agreement found, but with gaps in authority, freshness, full consensus, or source reachability. |
| ❌ **Unverified** | `unverified` | Insufficient evidence, low agreement, or sources failed retrieval. |

---

## 🤝 Consensus Engine Explanation

The Consensus Engine *(current implementation)* compares claims extracted from **multiple independent sources** for the same query and computes an **agreement score** — a measure of how much those sources actually corroborate one another.

This is the mechanism that directly addresses the "no disagreement detection" failure mode described in [Why Existing AI Hallucinates](#-why-existing-ai-hallucinates): if sources disagree, that disagreement is captured in the score rather than silently discarded. This module is functional today and is actively being improved.

---

## 🕒 Freshness Score Explanation

The Freshness Score *(basic)* estimates how recent a claim or its source is. The **current implementation is a basic heuristic** (e.g., based on available date metadata where present) and is explicitly **not** a comprehensive temporal-relevance system yet. More advanced freshness modeling is tracked under [Phase A — VRA Engine Hardening](#-future-roadmap-phased).

---

## 🏅 Authority Score Explanation

The Authority Score *(basic)* reflects how authoritative a source domain is considered to be, derived from its classification within the [Source Registry](#-source-registry). Sources are not all treated equally — a registry entry's authority weighting directly affects how much its claims influence the final Trust Score.

---

## 🛡️ Guardrails

The **Anti-Hallucination Guard** *(rule-based implementation)* is the system's last line of defense before an answer reaches the user. It is responsible for:

- Flagging or downgrading answers with low consensus
- Flagging or downgrading answers built from low-authority sources only
- Preventing the Answer Builder from presenting claims that aren't backed by extracted evidence as fully verified

> ⚠️ **Important:** The guard is currently **rule-based**, reduces — but does not eliminate — the risk of incorrect answers, and continues to be hardened. No verification system is infallible.

---

## 🗂️ Source Registry

The Source Registry is a structured catalog of trusted domains used by the Source Registry Loader and Source Selector. It lives under `source_registry/` and is intentionally kept as **data**, not hardcoded logic, so it can be reviewed, audited, and extended independently of the pipeline code.

---

## 🐞 Debug Mode

When enabled (via request flag or environment variable), Debug Mode exposes additional internal pipeline metadata in API responses — such as intermediate scores, the list of fetched URLs, and per-source extraction results — to aid development and troubleshooting.

```json
{
  "query": "Example query",
  "debug": true
}
```

---

## 📋 Current Implementation Status

### 🧩 Core Feature Grid

| Feature | Status |
|---|---|
| FastAPI Backend | ✅ Implemented |
| VRA Pipeline | ✅ Implemented |
| Intent Detection | ✅ Implemented |
| Source Registry | ✅ Implemented |
| Source Selection | ✅ Implemented |
| Query Retrieval | ✅ Implemented |
| Source Fetching | ✅ Implemented |
| Claim Extraction | ✅ Implemented |
| Consensus Engine | 🔄 Implemented / Improving |
| Trust Score Engine | 🔄 Implemented / Improving |
| Authority Score | 🟡 Basic |
| Freshness Score | 🟡 Basic |
| Anti-Hallucination Guard | 🟡 Rule-based |
| Evidence Summary | ✅ Implemented |
| Verification Metadata | ✅ Implemented |
| Debug Mode | ✅ Implemented |
| Evidence Graph | 📌 Planned |
| Knowledge Graph | 📌 Planned |
| Export Engine (PDF/PPT/DOCX) | 📌 Planned |
| ML Layer | 📌 Planned |
| Frontend UI | 🚧 Under Development |
| Admin Panel | 📌 Planned |
| Deployment | 📌 Planned |

**Legend:** ✅ Implemented · 🔄 Implemented and actively improving · 🟡 Basic/early implementation · 🚧 Under development · 📌 Planned only, not yet built

---

## 🕘 Version History

| Version | Milestone |
|---|---|
| v0.1 | Project initialization |
| v0.2 | FastAPI backend setup |
| v0.3 | VRA pipeline foundation |
| v0.4 | Source registry and source selection |
| v0.5 | Claim extraction and consensus engine |
| v0.6 | Trust score, authority score, and freshness score |
| v0.7 | Verification metadata and anti-hallucination guard |
| Current | Active development / pre-launch |

---

## 🛣️ Future Roadmap (Phased)

> ⚠️ **Everything in this section is planned only.** None of the items below exist in the current codebase. They are documented here to communicate direction, not current capability.

### 🚀 Upcoming Launch Features *(Planned)*

- Evidence Graph
- Claim Lineage
- Better contradiction detection
- Better source reliability memory
- Improved freshness scoring
- Frontend chat interface
- Source cards and evidence panels
- PDF report export
- PPT generation
- DOCX document export
- Math / Physics / Chemistry answer modules
- Graph and table rendering
- Admin dashboard
- Deployment pipeline

### 🔧 Phase A — VRA Engine Hardening
- [ ] Evidence Graph
- [ ] Claim Lineage
- [ ] Better contradiction detection
- [ ] Source reliability memory
- [ ] Better freshness scoring

### 🎨 Phase B — User Experience
- [ ] Frontend chat UI
- [ ] Source cards
- [ ] Evidence panels
- [ ] Verification badges (UI rendering)
- [ ] Graph/table rendering

### 📤 Phase C — Export Engine
- [ ] PDF reports
- [ ] PPT generation
- [ ] DOCX documents
- [ ] Excel/table export

### 🧪 Phase D — Subject-Specific Intelligence
- [ ] Math solver with graph rendering
- [ ] Physics problem solver
- [ ] Chemistry problem solver
- [ ] Research mode
- [ ] Student mode
- [ ] Expert mode

### 🤖 Phase E — ML Layer
- [ ] ML source ranking
- [ ] ML trust prediction
- [ ] Feedback learning
- [ ] Hallucination risk prediction

### 🏗️ Phase F — Production Infrastructure
- [ ] Docker
- [ ] Redis cache
- [ ] Monitoring
- [ ] Deployment
- [ ] CI/CD

### 🗺️ Development Phase Progress

| Phase | Name | Status |
|---|---|---|
| Phase 1 | Project Structure | ✅ Complete |
| Phase 2 | Backend FastAPI Setup | ✅ Complete |
| Phase 3 | Database Schema / Foundation | 🔄 In Progress |
| Phase 4 | VRA Core Algorithm | 🔄 In Progress |
| Phase 5 | Source Registry | 🔄 In Progress |
| Phase 6 | Trust Score Engine | 🔄 In Progress |
| Phase 7 | Answer Builder | 🔄 In Progress |
| Phase 8 | Frontend Chat UI | 📌 Planned |
| Phase 9 | Admin Panel | 📌 Planned |
| Phase 10 | ML Models | 📌 Planned |
| Phase 11 | Testing | 📌 Planned |
| Phase 12 | Deployment | 📌 Planned |

> 📝 **Note:** This project is under active development. The README separates implemented features from planned features to avoid overstating current capabilities.

---

## 🎯 Project Goals

- Complete all 12 development phases
- Launch a stable public beta
- Build a polished frontend chat UI
- Add Evidence Graph and Claim Lineage
- Add PDF, PPT, and DOCX export support
- Add subject-specific answer modules for Math, Physics, and Chemistry
- Add ML-powered source ranking and trust prediction
- Deploy the platform publicly
- Build a community around trustworthy AI search

---

## ⚠️ Known Limitations

- Some sources may block or rate-limit requests.
- Freshness metadata may not always be available from a given source.
- Trust score is a **heuristic**, not a mathematical guarantee of correctness.
- Current consensus logic is functional but still improving.
- The system is under **active development** and behavior may change between commits.

---

## 🖼️ Screenshots

UI screenshots will be published once the frontend reaches beta.

---

## 🎬 Demo

Live demo and deployment will be available after the first public beta release.

---

## 📈 Benchmarks

Benchmarking is planned after the first stable release. No formal benchmark numbers are published yet.

---

## 🎯 Performance Goals

These are **goals**, not measured results:

- Minimize end-to-end query latency while preserving multi-source verification.
- Maximize agreement-detection accuracy across heterogeneous source formats.
- Keep the Anti-Hallucination Guard's false-suppression rate low without compromising safety.

---

## 🔒 Security

- **Never commit `.env` files.** Use `.env.example` for safe variable templates.
- If a secret is **accidentally committed, rotate/revoke the key immediately** — do not assume removing it from a later commit is sufficient.
- Outbound requests to external sources should respect timeouts and reasonable rate limits to avoid abuse.
- Input validation is enforced at the API boundary via Pydantic models.

> 📌 A formal security policy and responsible disclosure process are planned but not yet published.

---

## 🧪 Testing

```bash
# From the project root
pytest
```

> 📌 Test coverage is actively being expanded (see [Phase 11 — Testing](#-future-roadmap-phased)). Contributions that add tests for existing VRA modules are especially welcome.

---

## 🚀 Deployment

> 📌 **Planned.** Formal deployment guides (Docker-based and otherwise) will be added once containerization work (see [Phase F](#-future-roadmap-phased)) is complete. No deployed instance currently exists. Currently, the project is intended to be run locally via Uvicorn as described in [Running the Backend](#-running-the-backend).

---

## ❓ FAQ

**Q: Is this a chatbot?**
A: No. It is a verification-first pipeline that produces answers only after running retrieval and consensus checks against trusted sources.

**Q: What is the main API endpoint?**
A: `POST /chat`. See [API Documentation](#-api-documentation) and [API Examples](#-api-examples).

**Q: Does it use a large language model internally?**
A: The Answer Builder stage is responsible for synthesizing verified claims into natural language. The emphasis of the project is on the verification pipeline surrounding generation, not on generation alone.

**Q: Is the Freshness Score fully accurate?**
A: No — it is explicitly a **basic heuristic** today, not a comprehensive temporal model. See [Freshness Score Explanation](#-freshness-score-explanation).

**Q: Are the ML features in the roadmap available now?**
A: No. All ML-related items (ranking, trust prediction, feedback learning) are **planned only** — see [Phase E — ML Layer](#-future-roadmap-phased).

**Q: Is every answer "Verified"?**
A: No. Answers can be Verified, Partially Verified, or Unverified depending on source agreement, reachability, and authority. See [Verification Levels](#-verification-levels).

---

## 🔧 Troubleshooting

| Issue | Possible Cause | Suggested Fix |
|---|---|---|
| `500 Internal Server Error` | Unhandled exception in the backend | Check the terminal traceback where Uvicorn is running for the actual error |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` inside an activated virtual environment |
| API endpoint not found | Wrong endpoint used | Use `POST /chat`, not `/api/query` |
| Swagger UI not opening | Backend not running | Ensure `uvicorn backend.app.main:app --reload` is running and check the terminal for startup errors |
| Missing `.env` values | `.env` not created from template | Run `cp .env.example .env` and fill in the required values |
| Fetch errors / timeouts | Network restrictions or slow source response | Check `REQUEST_TIMEOUT_SECONDS` and target source availability |

---

## 🌟 Project Highlights

This project demonstrates:

- AI system design
- Information retrieval
- Evidence-based verification
- Source ranking
- API design
- Modular backend architecture
- Responsible AI principles
- Explainable AI response design

The codebase is structured to make a clear, auditable distinction between **what is currently implemented** and **what is planned**, in line with responsible disclosure of system capabilities.

---

## 🤲 Contributing

Contributions are welcome — this is an actively developing open-source project.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

> 💡 **Tip:** When contributing a new VRA module or modifying an existing one, please document what problem it solves, consistent with the rest of this README.
>
> 🧷 Before pushing, double-check that no `.env` file or other secret is staged for commit.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 📑 Citation

If you reference this project in academic or research work, please cite it as:

```bibtex
@software{authentic_ai_search,
  author  = {Abhinav Ankit},
  title   = {Authentic AI Search: An AI Verification Engine using the Verified Resource Algorithm (VRA)},
  year    = {2025},
  url     = {https://github.com/AbhinavXor/authentic-ai-search}
}
```

---

## 🙏 Acknowledgements

- Built using the open-source **FastAPI**, **Pydantic**, **Requests**, and **BeautifulSoup4** ecosystems.
- Inspired by the broader open-source AI infrastructure community's work on retrieval-augmented and evidence-grounded systems.

---

## 👤 Author

**Abhinav Ankit**
GitHub: [@AbhinavXor](https://github.com/AbhinavXor)

Project creator and maintainer of Authentic AI Search.

---

## 📬 Contact

For questions, suggestions, or collaboration inquiries, please open an issue on the [repository](https://github.com/AbhinavXor/authentic-ai-search) or reach out via the contact details on the author's GitHub profile.

---

<div align="center">

Made with ❤️ by **Abhinav Ankit**

⭐ GitHub:
https://github.com/AbhinavXor/authentic-ai-search

**Authentic AI Search**
*Trust before Intelligence.*

Powered by **VRA — Verified Resource Algorithm**

**Authentic AI Search**
*Trust before Intelligence.*

Powered by **VRA — Verified Resource Algorithm**

</div>