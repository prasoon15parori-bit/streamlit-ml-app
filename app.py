
import streamlit as st
from datetime import datetime, date, time, timedelta
import pandas as pd
import json, html, re

# ==========================================================
# CAMPUSAI — FULL FLEDGED FRONTEND PROTOTYPE
# ==========================================================

st.set_page_config(
    page_title="CampusAI",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------- CSS ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.stApp { background:#f4f7fb; }
.block-container { max-width:1400px; padding-top:1.2rem; }

section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0d1833 0%,#162b58 100%);
}
section[data-testid="stSidebar"] * { color:#f6f8ff !important; }

.hero {
    background:linear-gradient(135deg,#12244f,#2858d5);
    color:#fff; padding:27px 30px; border-radius:22px;
    box-shadow:0 14px 35px rgba(26,69,170,.18); margin-bottom:20px;
}
.hero h1 { color:#fff; font-size:31px; margin:0; font-weight:800; }
.hero p { color:#dce7ff; margin:5px 0 0; font-size:14px; }

.card {
    background:#fff; border:1px solid #e4e9f2; border-radius:17px;
    padding:18px; box-shadow:0 5px 18px rgba(23,35,59,.045);
    margin-bottom:13px;
}
.metric {
    background:#fff; border:1px solid #e4e9f2; border-radius:17px;
    padding:17px; box-shadow:0 5px 18px rgba(23,35,59,.045);
}
.metric-value {font-size:29px;font-weight:800;color:#204dbb;}
.metric-label {font-size:12px;color:#718096;}
.card-title {font-size:16px;font-weight:750;color:#172033;}
.muted {font-size:12px;color:#718096;}

.badge {
 display:inline-block;padding:4px 9px;border-radius:20px;
 font-size:11px;font-weight:700;margin-right:4px;
}
.red{background:#ffe7ed;color:#c72f55}.orange{background:#fff0d7;color:#a96b00}
.green{background:#def8ed;color:#087b57}.blue{background:#e5edff;color:#2854b7}
.purple{background:#eee6ff;color:#6c3db7}

.notice-high{border-left:5px solid #ed476e}.notice-medium{border-left:5px solid #f2a43a}
.notice-low{border-left:5px solid #20b486}

div[data-testid="stMetric"] {
    background:white;border:1px solid #e4e9f2;border-radius:15px;padding:10px;
}
.stButton>button {border-radius:10px;font-weight:650;}
.footer{text-align:center;color:#8995a8;font-size:11px;padding:25px 0;}
.smallcaps{font-size:11px;color:#718096;text-transform:uppercase;letter-spacing:.7px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ---------------------- DATA / STATE -----------------------
def seed_notices():
    now = datetime.now()
    return [
        {"id":1,"title":"Internship Preference Form","category":"Internship","priority":"High",
         "deadline":(date.today()+timedelta(days=0)).isoformat()+" 17:00",
         "audience":"AI/ML","description":"Eligible students must submit the internship preference form.",
         "status":"Active","created":"Today"},
        {"id":2,"title":"BEEE Assignment Submission","category":"Academic","priority":"Medium",
         "deadline":(date.today()+timedelta(days=3)).isoformat()+" 23:59",
         "audience":"All Students","description":"Submit the BEEE assignment through the department portal.",
         "status":"Active","created":"Today"},
        {"id":3,"title":"AI/ML Hackathon Registration","category":"Hackathon","priority":"High",
         "deadline":(date.today()+timedelta(days=6)).isoformat()+" 18:00",
         "audience":"AI/ML","description":"Students interested in AI/ML can register for the upcoming hackathon.",
         "status":"Active","created":"Today"},
        {"id":4,"title":"Department Meeting","category":"Event","priority":"Low",
         "deadline":(date.today()+timedelta(days=8)).isoformat()+" 12:00",
         "audience":"CRs","description":"Class representatives should attend the department coordination meeting.",
         "status":"Active","created":"Today"}
    ]

def seed_students():
    names=["Aarav","Riya","Kunal","Mehak","Dev","Ananya","Arjun","Isha","Kabir","Nisha","Vihaan","Sara"]
    statuses=["Completed","Completed","Pending","Pending","Completed","Pending","Completed","Completed","Pending","Completed","Pending","Completed"]
    rows=[]
    for i,(n,s) in enumerate(zip(names,statuses),1):
        rows.append({"Roll No":f"24AIML{i:02d}","Name":n,"Branch":"AI/ML",
                     "Semester":"4th","Status":s,"Last Active":"Today" if s=="Completed" else "Yesterday",
                     "Risk":"Low" if s=="Completed" else ("High" if i%2 else "Medium")})
    return rows

def seed_opportunities():
    return [
        {"id":1,"title":"AI Research Internship","type":"Internship","skills":"Python, ML, NLP","deadline":str(date.today()+timedelta(days=12)),"eligibility":"AI/ML"},
        {"id":2,"title":"Smart Campus Hackathon","type":"Hackathon","skills":"Python, Streamlit, APIs","deadline":str(date.today()+timedelta(days=8)),"eligibility":"All"},
        {"id":3,"title":"Data Science Workshop","type":"Workshop","skills":"Pandas, SQL, Visualization","deadline":str(date.today()+timedelta(days=5)),"eligibility":"AI/ML"},
        {"id":4,"title":"Frontend Developer Internship","type":"Internship","skills":"HTML, CSS, JavaScript","deadline":str(date.today()+timedelta(days=18)),"eligibility":"All"}
    ]

if "notices" not in st.session_state: st.session_state.notices=seed_notices()
if "students" not in st.session_state: st.session_state.students=seed_students()
if "opportunities" not in st.session_state: st.session_state.opportunities=seed_opportunities()
if "reminders" not in st.session_state: st.session_state.reminders=[]
if "activity" not in st.session_state:
    st.session_state.activity=[("System","CampusAI initialized","Just now"),
                               ("CR","Internship Preference Form published","10 min ago")]
if "next_notice" not in st.session_state: st.session_state.next_notice=5
if "next_opp" not in st.session_state: st.session_state.next_opp=5
if "settings" not in st.session_state:
    st.session_state.settings={"quiet":True,"auto_summary":True,"auto_priority":True,"language":"English"}

# ---------------------- HELPERS ----------------------------
def esc(x): return html.escape(str(x))
def badge(text, cls="blue"): return f'<span class="badge {cls}">{esc(text)}</span>'
def pbadge(p): return badge(p+" Priority", {"High":"red","Medium":"orange","Low":"green"}.get(p,"blue"))
def nborder(p): return {"High":"notice-high","Medium":"notice-medium","Low":"notice-low"}.get(p,"")
def log(actor, action):
    st.session_state.activity.insert(0,(actor,action,"Just now"))
def stats():
    total=len(st.session_state.students)
    done=sum(s["Status"]=="Completed" for s in st.session_state.students)
    pending=total-done
    rate=round(done/total*100) if total else 0
    high=sum(s["Risk"]=="High" for s in st.session_state.students)
    return total,done,pending,rate,high
def df_students():
    return pd.DataFrame(st.session_state.students)
def ai_analyze(title, description, deadline):
    text=(title+" "+description).lower()
    if any(k in text for k in ["urgent","today","immediately","last date"]): priority="High"
    elif any(k in text for k in ["deadline","submit","registration","assignment"]): priority="Medium"
    else: priority="Low"
    cats={"internship":"Internship","hackathon":"Hackathon","exam":"Exam","assignment":"Academic",
          "attendance":"Academic","workshop":"Workshop","meeting":"Event","event":"Event"}
    category=next((v for k,v in cats.items() if k in text),"General")
    action="Complete the required action before the deadline."
    summary=(description[:155]+"...") if len(description)>155 else description
    return category,priority,summary,action

# ---------------------- SIDEBAR ----------------------------
st.sidebar.markdown(
    '<div style="font-size:27px;font-weight:800">CampusAI</div>'
    '<div style="font-size:12px;color:#b9c6df!important"></div>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
page=st.sidebar.radio("Navigation",[
    "Dashboard","Create Notice","Manage Notices","Students",
    "Student Portal","Opportunities","Analytics","Activity Log","Settings"
])


# ==========================================================
# DASHBOARD
# ==========================================================
if page=="Dashboard":
    st.markdown('<div class="hero"><h1>CR Command Center</h1><p>One place to publish, monitor, remind and understand student engagement.</p></div>',unsafe_allow_html=True)
    total,done,pending,rate,high=stats()
    c=st.columns(5)
    for col,val,label in zip(c,[total,done,pending,f"{rate}%",high],["Students","Completed","Pending","Response Rate","High Risk"]):
        with col: st.markdown(f'<div class="metric"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    l,r=st.columns([1.55,1])
    with l:
        st.subheader("Priority Feed")
        for n in st.session_state.notices[:5]:
            st.markdown(f'<div class="card {nborder(n["priority"])}"><div class="card-title">{esc(n["title"])}</div>{pbadge(n["priority"])} {badge(n["category"],"blue")}<p>{esc(n["description"])}</p><div class="muted">Deadline: <b>{esc(n["deadline"])}</b> • Audience: {esc(n["audience"])}</div></div>',unsafe_allow_html=True)
    with r:
        st.subheader("Quick Actions")
        if st.button("Create Notice",use_container_width=True): st.info("Use Create Notice in the sidebar.")
        if st.button("Send Pending Reminders",use_container_width=True):
            st.session_state.reminders.append({"notice":"Pending actions","count":pending,"time":datetime.now().strftime("%H:%M")})
            log("CR",f"Reminder prepared for {pending} pending students")
            st.success(f"Reminder prepared for {pending} students.")
        if st.button("Refresh Dashboard",use_container_width=True): st.rerun()
        st.subheader("Response Progress")
        st.progress(rate/100 if rate else 0)
        st.caption(f"{done} completed • {pending} pending")
        st.subheader("AI Alert")
        if high: st.warning(f"{high} students are currently marked high-risk in this demo. AI can prioritize follow-up.")
        else: st.success("No high-risk students.")
    st.divider()
    st.subheader("Latest Activity")
    for a,b,t in st.session_state.activity[:6]:
        st.markdown(f"**{a}** — {b}  \n<span class='muted'>{t}</span>",unsafe_allow_html=True)

# ==========================================================
# CREATE NOTICE
# ==========================================================
elif page=="Create Notice":
    st.markdown('<div class="hero"><h1>Create Smart Notice</h1><p>Build a notice with audience, deadline, priority and an AI-assisted interpretation.</p></div>',unsafe_allow_html=True)
    with st.form("notice_form"):
        title=st.text_input("Notice title",placeholder="e.g. Internship Preference Form")
        description=st.text_area("Message",height=130,placeholder="Write the full announcement...")
        c1,c2,c3=st.columns(3)
        category=c1.selectbox("Category",["Auto Detect","Academic","Exam","Internship","Hackathon","Event","Workshop","General"])
        priority=c2.selectbox("Priority",["Auto Detect","High","Medium","Low"])
        audience=c3.selectbox("Audience",["All Students","AI/ML","CSE","ECE","Civil","CRs"])
        d1,d2=st.columns(2)
        dd=d1.date_input("Deadline",date.today()+timedelta(days=2))
        dt=d2.time_input("Deadline time",time(17,0))
        submit=st.form_submit_button("Publish Notice",use_container_width=True)
    if submit:
        if not title.strip() or not description.strip(): st.error("Title and message are required.")
        else:
            auto_cat,auto_pr,summary,action=ai_analyze(title,description,str(dd))
            final_cat=auto_cat if category=="Auto Detect" else category
            final_pr=auto_pr if priority=="Auto Detect" else priority
            deadline=f"{dd.isoformat()} {dt.strftime('%H:%M')}"
            st.session_state.notices.insert(0,{"id":st.session_state.next_notice,"title":title,"category":final_cat,"priority":final_pr,
                "deadline":deadline,"audience":audience,"description":description,"status":"Active","created":"Just now"})
            st.session_state.next_notice+=1
            log("CR",f"Published: {title}")
            st.success("Notice published successfully.")
            a,b=st.columns(2)
            with a:
                st.markdown(f'<div class="card"><div class="card-title">AI Classification</div>{badge(final_cat,"purple")} {pbadge(final_pr)}<p>{esc(summary)}</p><div class="muted">Suggested action: {esc(action)}</div></div>',unsafe_allow_html=True)
            with b:
                st.markdown(f'<div class="card"><div class="card-title">Delivery Plan</div><p>Audience: <b>{esc(audience)}</b></p><p>Deadline: <b>{esc(deadline)}</b></p><p>Smart reminder: <b>Enabled</b></p></div>',unsafe_allow_html=True)
    st.divider()
    st.subheader("AI Processing Preview")
    x,y,z=st.columns(3)
    x.info("Classification\n\nNLP can identify the notice category.")
    y.info("Deadline Extraction\n\nDates and times can be extracted from free text.")
    z.info("Priority Detection\n\nUrgency can be estimated from content + deadline.")

# ==========================================================
# MANAGE NOTICES
# ==========================================================
elif page=="Manage Notices":
    st.markdown('<div class="hero"><h1>Notice Management</h1><p>Search, filter, edit, duplicate, archive or permanently delete notices.</p></div>',unsafe_allow_html=True)
    q=st.text_input("Search notices",placeholder="Search title, category, audience...")
    fc=st.selectbox("Category",["All"]+sorted(set(n["category"] for n in st.session_state.notices)))
    fp=st.selectbox("Priority",["All","High","Medium","Low"])
    visible=[n for n in st.session_state.notices if
             (not q or q.lower() in (n["title"]+" "+n["description"]+" "+n["category"]+" "+n["audience"]).lower())
             and (fc=="All" or n["category"]==fc) and (fp=="All" or n["priority"]==fp)]
    st.caption(f"{len(visible)} notice(s) shown")
    for n in list(visible):
        with st.expander(f'{n["title"]}  •  {n["category"]}  •  {n["priority"]}'):
            st.write(n["description"])
            st.caption(f'Deadline: {n["deadline"]} | Audience: {n["audience"]} | Status: {n["status"]}')
            c1,c2,c3,c4=st.columns(4)
            if c1.button("Delete",key=f"del{n['id']}"):
                st.session_state.notices=[x for x in st.session_state.notices if x["id"]!=n["id"]]
                log("CR",f"Deleted notice: {n['title']}")
                st.success("Deleted.")
                st.rerun()
            if c2.button("Duplicate",key=f"dup{n['id']}"):
                cp=dict(n); cp["id"]=st.session_state.next_notice; cp["title"]="Copy - "+cp["title"]
                st.session_state.next_notice+=1; st.session_state.notices.insert(0,cp)
                log("CR",f"Duplicated notice: {n['title']}")
                st.success("Duplicated.")
                st.rerun()
            if c3.button("Archive",key=f"arc{n['id']}"):
                for x in st.session_state.notices:
                    if x["id"]==n["id"]: x["status"]="Archived"
                log("CR",f"Archived notice: {n['title']}")
                st.success("Archived.")
                st.rerun()
            if c4.button("Copy Text",key=f"copy{n['id']}"):
                st.code(n["description"],language="text")
    st.divider()
    if st.button("Delete ALL Notices"):
        st.session_state.confirm_all=True
    if st.session_state.get("confirm_all"):
        st.error("This deletes all demo notices from the current session.")
        a,b=st.columns(2)
        if a.button("Confirm Delete All"):
            st.session_state.notices=[]; st.session_state.confirm_all=False; log("CR","Deleted all notices"); st.rerun()
        if b.button("Cancel"): st.session_state.confirm_all=False; st.rerun()

# ==========================================================
# STUDENTS
# ==========================================================
elif page=="Students":
    st.markdown('<div class="hero"><h1>Student Management</h1><p>Search students, inspect response status and identify follow-up priority.</p></div>',unsafe_allow_html=True)
    q=st.text_input("Search student",placeholder="Name or roll number")
    risk=st.selectbox("Risk filter",["All","High","Medium","Low"])
    rows=[s for s in st.session_state.students if (not q or q.lower() in (s["Name"]+s["Roll No"]).lower()) and (risk=="All" or s["Risk"]==risk)]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    st.subheader("Student Actions")
    selected=st.selectbox("Select student",[s["Roll No"]+" — "+s["Name"] for s in st.session_state.students])
    rr=next(s for s in st.session_state.students if s["Roll No"]==selected.split(" — ")[0])
    c1,c2,c3=st.columns(3)
    if c1.button("Mark Completed"):
        rr["Status"]="Completed"; rr["Risk"]="Low"; rr["Last Active"]="Now"; log("CR",f"Updated {rr['Name']} to Completed"); st.rerun()
    if c2.button("Mark Pending"):
        rr["Status"]="Pending"; rr["Risk"]="Medium"; log("CR",f"Updated {rr['Name']} to Pending"); st.rerun()
    if c3.button("Send Reminder"):
        st.session_state.reminders.append({"notice":"Direct student reminder","count":1,"time":datetime.now().strftime("%H:%M")})
        log("CR",f"Reminder sent to {rr['Name']}"); st.success("Reminder prepared.")

# ==========================================================
# STUDENT PORTAL
# ==========================================================
elif page=="Student Portal":
    st.markdown('<div class="hero"><h1>Student Portal</h1><p>A focused student experience: see what matters, act, and track completion.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns([1,2])
    with c1:
        name=st.text_input("Student name","Palpal")
        roll=st.text_input("Roll number","24AIML01")
        st.selectbox("Language",["English","Hindi + English"])
    with c2:
        st.subheader("My Important Notices")
        for n in [x for x in st.session_state.notices if x["status"]=="Active"][:4]:
            st.markdown(f'<div class="card {nborder(n["priority"])}"><div class="card-title">{esc(n["title"])}</div>{pbadge(n["priority"])} {badge(n["category"])}<p>{esc(n["description"])}</p><div class="muted">Deadline: {esc(n["deadline"])}</div></div>',unsafe_allow_html=True)
    st.subheader("Respond to Latest Notice")
    if st.session_state.notices:
        n=st.session_state.notices[0]
        response=st.radio(f'Have you completed "{n["title"]}"?',["Yes, Completed","Not Yet"],horizontal=True)
        if st.button("Submit Response",use_container_width=True):
            if response=="Yes, Completed":
                # demo: update first pending student
                target=next((s for s in st.session_state.students if s["Status"]=="Pending"),None)
                if target:
                    target["Status"]="Completed"; target["Risk"]="Low"; target["Last Active"]="Now"
                log("Student",f"{name} submitted a response for {n['title']}")
                st.success("Response submitted. Your status is updated.")
            else:
                st.warning("You remain pending. A reminder can be scheduled before the deadline.")

# ==========================================================
# OPPORTUNITIES
# ==========================================================
elif page=="Opportunities":
    st.markdown('<div class="hero"><h1>Opportunities Hub</h1><p>Hackathons, internships and workshops — with simple rule-based matching for this prototype.</p></div>',unsafe_allow_html=True)
    skill=st.text_input("Your skills", "Python, Streamlit, ML")
    for o in st.session_state.opportunities:
        score=sum(1 for s in [x.strip().lower() for x in skill.split(",")] if s and s in o["skills"].lower())
        score=min(98,45+score*20)
        st.markdown(f'<div class="card"><div class="card-title">{esc(o["title"])}</div>{badge(o["type"],"purple")}<p>Skills: {esc(o["skills"])}</p><div class="muted">Deadline: {esc(o["deadline"])} • Eligibility: {esc(o["eligibility"])}</div><p><b>Match score: {score}%</b></p></div>',unsafe_allow_html=True)

# ==========================================================
# ANALYTICS
# ==========================================================
elif page=="Analytics":
    st.markdown('<div class="hero"><h1>Engagement Analytics</h1><p>Turn communication activity into actionable information for CRs and faculty.</p></div>',unsafe_allow_html=True)
    total,done,pending,rate,high=stats()
    c=st.columns(4)
    c[0].metric("Response Rate",f"{rate}%"); c[1].metric("Pending",pending); c[2].metric("High Risk",high); c[3].metric("Notices",len(st.session_state.notices))
    st.subheader("Response Status")
    st.bar_chart(pd.DataFrame({"Students":[done,pending]},index=["Completed","Pending"]))
    st.subheader("Notice Categories")
    cats={}
    for n in st.session_state.notices: cats[n["category"]]=cats.get(n["category"],0)+1
    if cats: st.bar_chart(pd.Series(cats))
    st.subheader("Risk Distribution")
    risks={}
    for s in st.session_state.students: risks[s["Risk"]]=risks.get(s["Risk"],0)+1
    st.bar_chart(pd.Series(risks))
    st.subheader("Export Data")
    d1=df_students()
    st.download_button("Download Student CSV",d1.to_csv(index=False),"campusai_students.csv","text/csv")
    d2=pd.DataFrame(st.session_state.notices)
    st.download_button("Download Notices CSV",d2.to_csv(index=False),"campusai_notices.csv","text/csv")

# ==========================================================
# ACTIVITY LOG
# ==========================================================
elif page=="Activity Log":
    st.markdown('<div class="hero"><h1>Activity Log</h1><p>Track what the demo system and users have done.</p></div>',unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.activity,columns=["Actor","Action","Time"]),use_container_width=True,hide_index=True)
    if st.button("Clear Activity Log"):
        st.session_state.activity=[]; st.rerun()

# ==========================================================
# SETTINGS
# ==========================================================
else:
    st.markdown('<div class="hero"><h1>CampusAI Settings</h1><p>Configure the prototype experience before backend integration.</p></div>',unsafe_allow_html=True)
    st.session_state.settings["quiet"]=st.toggle("Respect quiet hours",st.session_state.settings["quiet"])
    st.session_state.settings["auto_summary"]=st.toggle("AI auto-summary",st.session_state.settings["auto_summary"])
    st.session_state.settings["auto_priority"]=st.toggle("AI priority suggestion",st.session_state.settings["auto_priority"])
    st.session_state.settings["language"]=st.selectbox("Default language",["English","Hindi + English"],index=0 if st.session_state.settings["language"]=="English" else 1)
    st.divider()
    st.subheader("Demo Data Controls")
    a,b=st.columns(2)
    if a.button("Reset Demo Data"):
        for k in ["notices","students","opportunities","reminders","activity"]:
            st.session_state.pop(k,None)
        st.rerun()
    if b.button("Export All JSON"):
        payload={"notices":st.session_state.notices,"students":st.session_state.students,"opportunities":st.session_state.opportunities}
        st.download_button("Download JSON",json.dumps(payload,indent=2),"campusai_data.json","application/json")

st.markdown('<div class="footer">CampusAI — Python + Streamlit + HTML/CSS + UI Design • Frontend Prototype</div>',unsafe_allow_html=True)
