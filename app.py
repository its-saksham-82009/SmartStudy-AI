import random
from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartStudy AI", page_icon="📚", layout="wide")

# -------------------- Question bank: 30 original practice questions --------------------
QUESTIONS = [
    # Physics (15)
    {"id":"PHY_013","subject":"Physics","topic":"Work, Energy and Power","difficulty":"Easy","q":"What is the SI unit of work?","options":["Newton","Joule","Watt","Pascal"],"answer":"Joule","explanation":"Work is measured in joules (J)."},
    {"id":"PHY_014","subject":"Physics","topic":"Laws of Motion","difficulty":"Easy","q":"A body starts from rest and accelerates at 2 m/s² for 3 s. What is its final speed?","options":["3 m/s","5 m/s","6 m/s","9 m/s"],"answer":"6 m/s","explanation":"v = u + at = 0 + 2×3 = 6 m/s."},
    {"id":"PHY_015","subject":"Physics","topic":"Units and Measurements","difficulty":"Easy","q":"Which of these is a scalar quantity?","options":["Displacement","Velocity","Speed","Force"],"answer":"Speed","explanation":"Speed has magnitude only, so it is scalar."},
    {"id":"PHY_016","subject":"Physics","topic":"Kinematics","difficulty":"Easy","q":"The slope of a position-time graph represents:","options":["Acceleration","Velocity","Force","Momentum"],"answer":"Velocity","explanation":"The slope gives change in position per unit time."},
    {"id":"PHY_017","subject":"Physics","topic":"Laws of Motion","difficulty":"Easy","q":"Which law explains why passengers jerk forward when a moving bus stops suddenly?","options":["Newton's first law","Newton's second law","Newton's third law","Law of gravitation"],"answer":"Newton's first law","explanation":"Inertia tends to keep the passenger moving forward."},
    {"id":"PHY_018","subject":"Physics","topic":"Work, Energy and Power","difficulty":"Medium","q":"A 2 kg object moves at 3 m/s. Its kinetic energy is:","options":["3 J","6 J","9 J","18 J"],"answer":"9 J","explanation":"KE = ½mv² = ½×2×9 = 9 J."},
    {"id":"PHY_019","subject":"Physics","topic":"Laws of Motion","difficulty":"Medium","q":"A net force of 12 N acts on a 3 kg body. Find its acceleration.","options":["2 m/s²","3 m/s²","4 m/s²","6 m/s²"],"answer":"4 m/s²","explanation":"a = F/m = 12/3 = 4 m/s²."},
    {"id":"PHY_020","subject":"Physics","topic":"Circular Motion","difficulty":"Medium","q":"For a car moving on a level circular road, the centripetal force is usually provided by:","options":["Weight","Normal reaction","Friction","Air pressure"],"answer":"Friction","explanation":"Static friction acts towards the centre of the circular path."},
    {"id":"PHY_021","subject":"Physics","topic":"Vectors","difficulty":"Medium","q":"Two perpendicular vectors have magnitudes 3 and 4. The magnitude of their resultant is:","options":["1","5","7","12"],"answer":"5","explanation":"R = √(3² + 4²) = 5."},
    {"id":"PHY_022","subject":"Physics","topic":"Kinematics","difficulty":"Medium","q":"A car's velocity changes from 10 m/s to 20 m/s in 5 s. Its average acceleration is:","options":["2 m/s²","5 m/s²","6 m/s²","10 m/s²"],"answer":"2 m/s²","explanation":"a = (20 − 10)/5 = 2 m/s²."},
    {"id":"PHY_023","subject":"Physics","topic":"Laws of Motion","difficulty":"Hard","q":"A 5 kg block on a frictionless surface is pulled by a 20 N horizontal force. Its acceleration is:","options":["2 m/s²","4 m/s²","5 m/s²","100 m/s²"],"answer":"4 m/s²","explanation":"Newton's second law: a = F/m = 20/5 = 4 m/s²."},
    {"id":"PHY_024","subject":"Physics","topic":"Work, Energy and Power","difficulty":"Hard","q":"A 2 kg body falls from rest through 5 m. Taking g = 10 m/s² and neglecting air resistance, its speed just before impact is:","options":["5 m/s","10 m/s","15 m/s","20 m/s"],"answer":"10 m/s","explanation":"v² = 2gh = 2×10×5 = 100, so v = 10 m/s."},
    {"id":"PHY_025","subject":"Physics","topic":"Circular Motion","difficulty":"Hard","q":"A body moves in a circle of radius 2 m at 4 m/s. Its centripetal acceleration is:","options":["2 m/s²","4 m/s²","8 m/s²","16 m/s²"],"answer":"8 m/s²","explanation":"a = v²/r = 16/2 = 8 m/s²."},
    {"id":"PHY_026","subject":"Physics","topic":"Kinematics","difficulty":"Hard","q":"A ball is thrown vertically upward at 20 m/s. Take g = 10 m/s². Time to reach its highest point is:","options":["1 s","2 s","3 s","4 s"],"answer":"2 s","explanation":"At the highest point v = 0; t = u/g = 20/10 = 2 s."},
    {"id":"PHY_027","subject":"Physics","topic":"Laws of Motion","difficulty":"Hard","q":"A 2 kg object experiences a net force of 10 N for 3 s. Its change in momentum is:","options":["10 kg m/s","15 kg m/s","30 kg m/s","60 kg m/s"],"answer":"30 kg m/s","explanation":"Change in momentum = impulse = FΔt = 10×3 = 30 kg m/s."},
    # Chemistry (10)
    {"id":"CHE_011","subject":"Chemistry","topic":"Atomic Structure","difficulty":"Easy","q":"The maximum number of electrons in the first shell is:","options":["2","8","18","32"],"answer":"2","explanation":"The first shell has n = 1, so maximum electrons = 2n² = 2."},
    {"id":"CHE_012","subject":"Chemistry","topic":"Chemical Bonding","difficulty":"Easy","q":"Which bond is formed by sharing electron pairs?","options":["Ionic","Covalent","Metallic","Hydrogen"],"answer":"Covalent","explanation":"Covalent bonds form when atoms share electron pairs."},
    {"id":"CHE_013","subject":"Chemistry","topic":"Periodic Table","difficulty":"Easy","q":"Elements in the same group generally have the same number of:","options":["Neutrons","Electron shells","Valence electrons","Isotopes"],"answer":"Valence electrons","explanation":"For main-group elements, group number relates to valence-electron count."},
    {"id":"CHE_014","subject":"Chemistry","topic":"Mole Concept","difficulty":"Easy","q":"The SI unit for amount of substance is:","options":["Gram","Mole","Litre","Kilogram"],"answer":"Mole","explanation":"The mole is the SI unit for amount of substance."},
    {"id":"CHE_015","subject":"Chemistry","topic":"Atomic Structure","difficulty":"Easy","q":"Which subatomic particle has a negative charge?","options":["Proton","Neutron","Electron","Nucleus"],"answer":"Electron","explanation":"An electron carries a negative elementary charge."},
    {"id":"CHE_016","subject":"Chemistry","topic":"Mole Concept","difficulty":"Medium","q":"How many moles are present in 18 g of water? (Molar mass = 18 g/mol)","options":["0.5 mol","1 mol","2 mol","18 mol"],"answer":"1 mol","explanation":"n = mass/molar mass = 18/18 = 1 mol."},
    {"id":"CHE_017","subject":"Chemistry","topic":"Chemical Bonding","difficulty":"Medium","q":"The shape of a methane (CH₄) molecule is:","options":["Linear","Trigonal planar","Tetrahedral","Bent"],"answer":"Tetrahedral","explanation":"Four bonding pairs around carbon arrange tetrahedrally."},
    {"id":"CHE_018","subject":"Chemistry","topic":"Atomic Structure","difficulty":"Medium","q":"The number of orbitals in a p subshell is:","options":["1","2","3","5"],"answer":"3","explanation":"A p subshell has three orbitals: px, py and pz."},
    {"id":"CHE_019","subject":"Chemistry","topic":"Periodic Table","difficulty":"Medium","q":"Across a period from left to right, atomic radius generally:","options":["Increases","Decreases","Stays exactly constant","First doubles"],"answer":"Decreases","explanation":"Effective nuclear charge generally increases across a period."},
    {"id":"CHE_020","subject":"Chemistry","topic":"Chemical Bonding","difficulty":"Medium","q":"Which molecule has a linear shape?","options":["H₂O","NH₃","CO₂","CH₄"],"answer":"CO₂","explanation":"CO₂ has two electron domains around carbon and is linear."},
    # Maths (5)
    {"id":"MAT_011","subject":"Maths","topic":"Trigonometry","difficulty":"Easy","q":"What is sin 30°?","options":["0","1/2","√3/2","1"],"answer":"1/2","explanation":"sin 30° = 1/2."},
    {"id":"MAT_012","subject":"Maths","topic":"Permutations","difficulty":"Easy","q":"What is 3!?","options":["3","6","9","12"],"answer":"6","explanation":"3! = 3×2×1 = 6."},
    {"id":"MAT_013","subject":"Maths","topic":"Quadratic Equations","difficulty":"Medium","q":"The roots of x² − 5x + 6 = 0 are:","options":["1 and 6","2 and 3","−2 and −3","0 and 5"],"answer":"2 and 3","explanation":"x² − 5x + 6 = (x − 2)(x − 3)."},
    {"id":"MAT_014","subject":"Maths","topic":"Permutations","difficulty":"Medium","q":"How many ways can 3 different books be arranged in a row?","options":["3","6","9","27"],"answer":"6","explanation":"The number of arrangements is 3! = 6."},
    {"id":"MAT_015","subject":"Maths","topic":"Trigonometry","difficulty":"Hard","q":"If sin θ = 3/5 and θ is acute, then cos θ equals:","options":["2/5","3/4","4/5","5/4"],"answer":"4/5","explanation":"cos θ = √(1 − sin²θ) = √(16/25) = 4/5."},
    {"id":"MAT_016","subject":"Maths","topic":"Trigonometry","difficulty":"Easy","q":"What is cos 60°?","options":["0","1/2","√3/2","1"],"answer":"1/2","explanation":"cos 60° = 1/2."},
    {"id":"MAT_017","subject":"Maths","topic":"Quadratic Equations","difficulty":"Easy","q":"Which of these is a root of x² − 9 = 0?","options":["1","2","3","4"],"answer":"3","explanation":"x² = 9, so x = 3 or x = −3; 3 is one root."},
    {"id":"MAT_018","subject":"Maths","topic":"Permutations","difficulty":"Medium","q":"How many distinct arrangements can be made using all letters of the word CAT?","options":["3","6","9","12"],"answer":"6","explanation":"All three letters are different, so the number of arrangements is 3! = 6."},
    {"id":"MAT_019","subject":"Maths","topic":"Sequences and Series","difficulty":"Medium","q":"What is the 5th term of the arithmetic sequence 2, 5, 8, 11, ...?","options":["12","13","14","15"],"answer":"14","explanation":"The common difference is 3, so the 5th term is 2 + 4×3 = 14."},
    {"id":"MAT_020","subject":"Maths","topic":"Trigonometry","difficulty":"Hard","q":"If tan θ = 3/4 and θ is acute, what is sec θ?","options":["4/5","5/4","3/5","5/3"],"answer":"5/4","explanation":"Using a 3–4–5 triangle, sec θ = hypotenuse/adjacent = 5/4."},
]

def init_state():
    defaults = {
        "quiz_questions": [],
        "used_ids": [],
        "last_result": None,
        "attempts": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def start_quiz(subject_filter, difficulty_filter):
    used = set(st.session_state.used_ids)
    pool = [
        q for q in QUESTIONS
        if q["id"] not in used
        and (subject_filter == "All" or q["subject"] == subject_filter)
        and (difficulty_filter == "All" or q["difficulty"] == difficulty_filter)
    ]
    if len(pool) < 10:
        # If the chosen filter has too few unused questions, explain instead of silently repeating.
        return False, len(pool)
    st.session_state.quiz_questions = random.sample(pool, 10)
    st.session_state.last_result = None
    return True, 10

def build_plan(topic_results, available_minutes):
    if not topic_results:
        return pd.DataFrame(columns=["Topic", "Quiz Score", "Priority", "Revision Minutes"])
    rows = []
    for topic, stats in topic_results.items():
        pct = round(100 * stats["correct"] / max(1, stats["total"]))
        priority = "High" if pct < 50 else ("Medium" if pct < 80 else "Low")
        weight = {"High": 3, "Medium": 2, "Low": 1}[priority]
        rows.append({"Topic": topic, "Quiz Score": pct, "Priority": priority, "_weight": weight})
    total_weight = sum(row["_weight"] for row in rows) or 1
    for row in rows:
        row["Revision Minutes"] = int(available_minutes * row["_weight"] / total_weight)
    # Distribute any rounding remainder so total equals available minutes.
    used = sum(row["Revision Minutes"] for row in rows)
    for i in range(available_minutes - used):
        rows[i % len(rows)]["Revision Minutes"] += 1
    rows.sort(key=lambda r: ({"High": 0, "Medium": 1, "Low": 2}[r["Priority"]], r["Quiz Score"]))
    return pd.DataFrame([{k: v for k, v in row.items() if k != "_weight"} for row in rows])

init_state()

st.title("📚 SmartStudy AI")
st.subheader("Class 11 • AI Study Planner & Quiz")
st.write("Practice Physics, Chemistry and Maths. Your quiz results help create a topic-wise revision plan.")
st.info("Capstone prototype: the quiz and planner work locally in this app. Priority rules are educational demo logic, not a medical or guaranteed prediction system.")

tab_quiz, tab_planner, tab_progress, tab_about = st.tabs(
    ["📝 Smart Quiz", "📅 Study Planner", "📈 Progress", "ℹ️ About Project"]
)

with tab_quiz:
    st.markdown("### Random 10-question quiz")
    col1, col2 = st.columns(2)
    with col1:
        subject_filter = st.selectbox("Subject", ["All", "Physics", "Chemistry", "Maths"], key="subject_filter")
    with col2:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"], key="difficulty_filter")
    if st.button("🎲 Generate New Quiz", type="primary", use_container_width=True):
        ok, amount = start_quiz(subject_filter, difficulty_filter)
        if not ok:
            st.warning(f"Only {amount} unused questions match these filters. Choose broader filters or reset quiz history.")
        else:
            st.rerun()

    if st.session_state.quiz_questions:
        with st.form("quiz_form"):
            submitted_answers = {}
            for i, q in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{i+1}. ({q['subject']} • {q['difficulty']})**")
                st.write(q["q"])
                submitted_answers[q["id"]] = st.radio(
                    f"Choose an answer for Q{i+1}",
                    q["options"],
                    index=None,
                    key=f"answer_{q['id']}",
                    label_visibility="collapsed",
                )
                st.caption(f"Topic: {q['topic']}")
                st.divider()
            submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True)
        if submitted:
            correct_total = 0
            topic_results = {}
            details = []
            for q in st.session_state.quiz_questions:
                chosen = submitted_answers[q["id"]]
                correct = chosen == q["answer"]
                correct_total += int(correct)
                stats = topic_results.setdefault(q["topic"], {"correct": 0, "total": 0})
                stats["total"] += 1
                stats["correct"] += int(correct)
                details.append({
                    "Question": q["q"],
                    "Your Answer": chosen or "Not answered",
                    "Correct Answer": q["answer"],
                    "Result": "Correct" if correct else "Incorrect",
                    "Explanation": q["explanation"],
                    "Topic": q["topic"],
                })
            score = round(100 * correct_total / len(st.session_state.quiz_questions))
            st.session_state.last_result = {
                "score": score,
                "correct": correct_total,
                "total": len(st.session_state.quiz_questions),
                "topics": topic_results,
                "details": details,
                "minutes": 120,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            for q in st.session_state.quiz_questions:
                if q["id"] not in st.session_state.used_ids:
                    st.session_state.used_ids.append(q["id"])
            st.session_state.attempts.append({
                "Attempt": len(st.session_state.attempts) + 1,
                "Date": st.session_state.last_result["date"],
                "Score (%)": score,
                "Correct": f"{correct_total}/{len(st.session_state.quiz_questions)}",
            })
            st.success(f"Quiz submitted! Score: {correct_total}/{len(st.session_state.quiz_questions)} ({score}%).")
            st.dataframe(pd.DataFrame(details), use_container_width=True, hide_index=True)
            st.markdown("### AI-style revision plan")
            plan = build_plan(topic_results, 120)
            st.dataframe(plan, use_container_width=True, hide_index=True)
            st.caption("The quiz history is remembered during this active app session. If the hosted app restarts, session-only history may reset.")
    else:
        st.write("Tap **Generate New Quiz** to begin. The app will select 10 unused questions matching your filters.")

with tab_planner:
    st.markdown("### Make a study timetable")
    subjects = st.multiselect("Subjects to study", ["Physics", "Chemistry", "Maths"], default=["Physics", "Chemistry", "Maths"])
    available_minutes = st.slider("Available study time (minutes)", min_value=30, max_value=360, value=120, step=15)
    weak_topics_text = st.text_area(
        "Weak topics (one per line)",
        placeholder="Laws of Motion\nChemical Bonding\nPermutations",
        help="Write the chapters you want to revise first."
    )
    if st.button("📅 Create My Timetable", use_container_width=True):
        topics = [line.strip() for line in weak_topics_text.splitlines() if line.strip()]
        if not subjects:
            st.warning("Select at least one subject.")
        else:
            if not topics:
                topics = [{"Physics":"Physics revision","Chemistry":"Chemistry revision","Maths":"Maths revision"}[s] for s in subjects]
            weights = [3 if i < max(1, len(topics)//3) else 2 for i in range(len(topics))]
            total = sum(weights)
            mins = [available_minutes * w // total for w in weights]
            for i in range(available_minutes - sum(mins)):
                mins[i % len(mins)] += 1
            timetable = []
            elapsed = 0
            for topic, minutes in zip(topics, mins):
                start = f"{elapsed//60:02d}:{elapsed%60:02d}"
                elapsed += minutes
                end = f"{elapsed//60:02d}:{elapsed%60:02d}"
                timetable.append({"Topic": topic, "Start (elapsed)": start, "End (elapsed)": end, "Duration (min)": minutes})
            st.dataframe(pd.DataFrame(timetable), use_container_width=True, hide_index=True)
            st.success(f"Timetable created for {available_minutes} minutes.")

with tab_progress:
    st.markdown("### Your progress in this session")
    if st.session_state.attempts:
        history_df = pd.DataFrame(st.session_state.attempts)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        st.metric("Quizzes completed", len(st.session_state.attempts))
        st.metric("Questions used", len(st.session_state.used_ids))
        if len(history_df) > 1:
            st.line_chart(history_df.set_index("Attempt")["Score (%)"])
    else:
        st.write("Complete a quiz to see your progress here.")
    if st.button("Reset used-question history", help="Allows previously used questions to appear again in this active session."):
        st.session_state.used_ids = []
        st.session_state.quiz_questions = []
        st.session_state.last_result = None
        st.session_state.attempts = []
        st.success("Session quiz history reset.")

with tab_about:
    st.markdown("""
    **Project name:** SmartStudy AI Class 11

    **Problem statement:** Students may struggle to decide which chapters to revise first and how to divide their study time.

    **How this prototype works:**
    1. A question bank provides multiple-choice practice.
    2. The quiz calculates score and topic-wise performance.
    3. A simple rule-based priority system labels topics High, Medium or Low priority.
    4. The planner divides the selected study time across topics.

    **Important limitation:** This version uses transparent rules, not a trained production AI model. Its recommendations are a learning prototype and should be checked by the student.
    """)
    st.markdown("**Question bank:** 35 original practice questions • Physics (15), Chemistry (10) and Maths (10).")
    st.markdown("**Technology:** Python, Streamlit and Pandas.")
