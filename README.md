The Responsibility Lens — HJPI Scoring Tool
Human Judgment Preservation Index
By Aderayo Adelanwa | Ethentra Limited

What is the HJPI Tool?
The Human Judgment Preservation Index (HJPI) evaluates whether an AI system supports or erodes human judgment over time.

It scores any AI system across five dimensions and returns a Flourishing Verdict — telling you whether the system is safe to deploy, needs redesign, or should be rejected.

Built for AI practitioners, ethics reviewers, and B2B tech teams who need a fast, structured way to assess AI systems before deployment.

The Five Dimensions
#	Dimension	Question
1	Reasoning Transparency	Does the AI show its reasoning so users can evaluate the logic?
2	User Override Capability	Can users override the system — and do they actually use it?
3	Skill Development	Does regular use build user skills rather than dependency?
4	No Decision Outsourcing	Are users genuinely reviewing outputs, not just approving them?
5	Transparency at Use	Do users understand what the system does at point of use?
Flourishing Verdicts
Score	Verdict
85–100%	✅ PASS — Flourishing-Oriented
70–84%	⚠️ CONDITIONAL PASS
50–69%	🔧 REDESIGN REQUIRED
Below 50%	❌ FAIL — Reject Deployment
Versions
V1 — Scoring tool with CSV saving ✅
V2 — Radar chart visualisation ✅
V3 — Streamlit web interface ✅
How to Run
Web Interface (V3) — Recommended
pip install streamlit matplotlib numpy
streamlit run hjpi_app.py
Terminal Version (V1/V2)
python hjpi_tool.py
Output
Interactive scoring across five dimensions
Flourishing Verdict — Pass, Conditional, Redesign, or Fail
Radar chart visualisation
Downloadable CSV result
Downloadable PNG chart
Requirements
streamlit
matplotlib
numpy
Install all at once:

pip install streamlit matplotlib numpy
About
Ethentra Limited builds tools and frameworks for responsible AI adoption in B2B tech.

🌐 store.aderayoadelanwa.com
📧 contact@aderayoadelanwa.com
💼 LinkedIn
The Responsibility Lens is part of Ethentra's Human-Centered AI toolkit.