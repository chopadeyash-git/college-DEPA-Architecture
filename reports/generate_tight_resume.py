import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_tight_1page_resume(output_path):
    doc = docx.Document()

    # Ultra-clean 1-page margins (0.4" top/bottom, 0.5" left/right)
    for section in doc.sections:
        section.top_margin = Inches(0.38)
        section.bottom_margin = Inches(0.38)
        section.left_margin = Inches(0.50)
        section.right_margin = Inches(0.50)

    # Base font setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(9.5)
    font.color.rgb = RGBColor(30, 41, 59)

    def add_p(text="", space_before=0, space_after=1, line_spacing=1.05, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            p.add_run(text)
        return p

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title.upper())
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        
        # Bottom border line
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="94A3B8"/></w:pBdr>')
        pPr.append(pBdr)
        return p

    def add_item_header(left_title, left_sub, right_text):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        cell_l = table.cell(0, 0)
        cell_r = table.cell(0, 1)
        cell_l.width = Inches(5.6)
        cell_r.width = Inches(1.9)

        for cell in (cell_l, cell_r):
            tcPr = cell._tc.get_or_add_tcPr()
            tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>')
            tcPr.append(tcMar)

        p_l = cell_l.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(2.5)
        p_l.paragraph_format.space_after = Pt(0.5)
        p_l.paragraph_format.line_spacing = 1.05
        
        r1 = p_l.add_run(left_title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        
        if left_sub:
            r2 = p_l.add_run("  |  " + left_sub)
            r2.font.size = Pt(8.5)
            r2.font.italic = True
            r2.font.color.rgb = RGBColor(71, 85, 105)

        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_r.paragraph_format.space_before = Pt(2.5)
        p_r.paragraph_format.space_after = Pt(0.5)
        p_r.paragraph_format.line_spacing = 1.05
        
        r_r1 = p_r.add_run(right_text)
        r_r1.font.bold = True
        r_r1.font.size = Pt(8.5)
        r_r1.font.color.rgb = RGBColor(51, 65, 85)

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.0)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.left_indent = Inches(0.18)
        
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
            r_bold.font.size = Pt(9.0)
            r_bold.font.color.rgb = RGBColor(15, 23, 42)
        
        run = p.add_run(text)
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # =========================================================================
    # 1. HEADER (NAME + CONTACT INFO)
    # =========================================================================
    p_name = add_p(space_before=0, space_after=1, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_name = p_name.add_run("RONGALI RUPESH")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(16)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(15, 23, 42)

    p_contact = add_p(space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_c = p_contact.add_run("rupesh72111221@gmail.com   |   +91 93917 25373   |   linkedin.com/in/rupesh-r-84b183311   |   github.com/rupesh12k6")
    r_c.font.size = Pt(8.5)
    r_c.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # 2. PROFESSIONAL SUMMARY
    # =========================================================================
    add_section_header("Professional Summary")
    p_sum = add_p(space_before=1, space_after=2, line_spacing=1.06)
    r_s = p_sum.add_run(
        "Backend-focused Computer Science undergraduate skilled in Java and Spring Boot, with strong foundations in Data Structures, "
        "Algorithms, and Distributed Systems. Built production-style federated platforms (DEPA-compliant consent manager, recruitment "
        "portal, anti-spam API) featuring asymmetric cryptography (RS256/ECDH), secure microservices, and Redis caching. "
        "Solved 750+ DSA problems with multiple national coding contest wins."
    )
    r_s.font.size = Pt(9.0)

    # =========================================================================
    # 3. EDUCATION
    # =========================================================================
    add_section_header("Education")
    add_item_header(
        "B.Tech in Computer Science & Engineering",
        "Anil Neerukonda Institute of Technology & Sciences (ANITS), Visakhapatnam",
        "2023 – 2027  |  CGPA: 9.0 / 10.0"
    )

    # =========================================================================
    # 4. TECHNICAL SKILLS
    # =========================================================================
    add_section_header("Technical Skills")
    def add_skill_line(cat, items):
        p = add_p(space_before=0, space_after=1, line_spacing=1.05)
        r1 = p.add_run(cat + ": ")
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        r2 = p.add_run(items)
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(51, 65, 85)

    add_skill_line("Languages", "Java (17+), SQL, C, Python")
    add_skill_line("Backend & Security", "Spring Boot, Spring Security, Spring Data JPA, Hibernate, REST APIs, JJWT, RS256, ECDH, AES-128-GCM")
    add_skill_line("Databases & Architecture", "PostgreSQL, MySQL, Redis (Sorted Sets, TTL Caching), Distributed Systems, Rate Limiting, Microservices")
    add_skill_line("Developer Tools", "Git, GitHub, Docker, Postman, Maven, Linux/Bash")

    # =========================================================================
    # 5. TECHNICAL PROJECTS
    # =========================================================================
    add_section_header("Technical Projects")

    # Project 1: DEPA Consent Manager
    add_item_header(
        "DEPA Consent Manager & Credential Exchange",
        "Java 17, Spring Boot, RS256, ECDH, AES-GCM, Postgres, Docker",
        "github.com/rupesh12k6/DE_9_Infosys"
    )
    add_bullet("Architected a 3-tier federated consent platform compliant with India’s DEPA & DPDP framework, enabling data-blind, peer-to-peer academic credential exchange between autonomous university nodes.")
    add_bullet("Engineered an asymmetric trust engine using RS256 (RSA-2048) to mint tamper-proof access grant tokens, decoupling verification from database hits and ensuring non-repudiation across institutions.")
    add_bullet("Implemented end-to-end encrypted transport using ECDH (Secp256r1) key agreement and AES-128-GCM, guaranteeing the central Consent Manager remains strictly data-blind.")
    add_bullet("Built dual-layer verification coupling offline RS256 token validation with real-time synchronous introspection (<150ms), enforcing instant revocation and eliminating stale token abuse.")

    # Project 2: BotShield API
    add_item_header(
        "BotShield API — Anti-Spam Social Backend",
        "Java, Spring Boot, PostgreSQL, Redis, REST APIs, Concurrency",
        "github.com/rupesh12k6/BotShieldAPI"
    )
    add_bullet("Engineered an anti-spam social backend separating human users from automated bots via weighted engagement algorithms (+50 humans / +1 bots) to prioritize genuine content.")
    add_bullet("Implemented a bot cooldown system preventing automated reply-spam for 15-minute intervals using Redis key expiration (TTL).")
    add_bullet("Developed a real-time leaderboard using Redis Sorted Sets updated atomically on engagement, eliminating heavy repeated database count queries.")

    # Project 3: DriveFlow
    add_item_header(
        "DriveFlow — Campus Recruitment Platform",
        "Spring Boot, Spring Security, JWT, PostgreSQL, React, Docker",
        "github.com/rupesh12k6/DriveFlow_backend"
    )
    add_bullet("Built a multi-tenant recruitment platform supporting 4 distinct roles (Student/Company/Admin/Super Admin) with JWT-based RBAC.")
    add_bullet("Designed 50+ RESTful APIs managing the recruitment drive lifecycle with automated student eligibility filtering and shortlisting.")
    add_bullet("Optimized PostgreSQL queries with composite indexing and keyset pagination, handling large candidate datasets with low latency.")

    # =========================================================================
    # 6. WORK EXPERIENCE
    # =========================================================================
    add_section_header("Work Experience")
    add_item_header(
        "Java Developer Intern",
        "Ascendix Solutions",
        "May 2025 – June 2025  |  Visakhapatnam, India"
    )
    add_bullet("Engineered backend database modules using JDBC for high-throughput relational data operations with connection pooling.")
    add_bullet("Developed a real-time Currency Exchange application in Java integrating external live rate feeds from ExchangeRate-API.")

    # =========================================================================
    # 7. AWARDS & COMPETITIVE PROGRAMMING
    # =========================================================================
    add_section_header("Awards & Competitive Programming")
    add_bullet("Secured 1st Prize in TechNova National Coding Contest among participants nationwide.", "National Coding Champion: ")
    add_bullet("Secured 1st Place in Code Velocity Competitive Programming Event.", "1st Place: ")
    add_bullet("Solved 500+ problems on LeetCode and 250+ problems on GeeksforGeeks (Institute Rank 35).", "Competitive Problem Solving: ")
    add_bullet("Software Engineer (HackerRank)  |  Java (HackerRank)  |  SQL and Relational Databases 101 (IBM Skills Network).", "Certifications: ")

    doc.save(output_path)
    print(f"Successfully generated 1-page resume at: {output_path}")

if __name__ == '__main__':
    create_tight_1page_resume('reports/Rongali_Rupesh_Resume_1Page.docx')

