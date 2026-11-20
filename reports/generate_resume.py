import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_resume_docx(output_path):
    doc = docx.Document()

    # 0.5-inch margins for modern 1-page tech resume
    for section in doc.sections:
        section.top_margin = Inches(0.45)
        section.bottom_margin = Inches(0.45)
        section.left_margin = Inches(0.55)
        section.right_margin = Inches(0.55)

    # Base font setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(9.5)
    font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    def add_p(text="", space_before=0, space_after=2, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.LEFT):
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
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title.upper())
        run.font.name = 'Calibri'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        
        # Add bottom border under section header (standard ATS resume style)
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="94A3B8"/></w:pBdr>')
        pPr.append(pBdr)
        return p

    def add_item_header_2col(left_title, left_sub, right_text, right_sub=None):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        cell_l = table.cell(0, 0)
        cell_r = table.cell(0, 1)
        cell_l.width = Inches(5.3)
        cell_r.width = Inches(2.1)

        # Clear cell margins
        for cell in (cell_l, cell_r):
            tcPr = cell._tc.get_or_add_tcPr()
            tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>')
            tcPr.append(tcMar)

        p_l = cell_l.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(3)
        p_l.paragraph_format.space_after = Pt(1)
        p_l.paragraph_format.line_spacing = 1.05
        
        r1 = p_l.add_run(left_title)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        
        if left_sub:
            r2 = p_l.add_run("  |  " + left_sub)
            r2.font.size = Pt(9)
            r2.font.italic = True
            r2.font.color.rgb = RGBColor(71, 85, 105)

        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_r.paragraph_format.space_before = Pt(3)
        p_r.paragraph_format.space_after = Pt(1)
        p_r.paragraph_format.line_spacing = 1.05
        
        r_r1 = p_r.add_run(right_text)
        r_r1.font.bold = True
        r_r1.font.size = Pt(9)
        r_r1.font.color.rgb = RGBColor(51, 65, 85)
        
        if right_sub:
            p_r2 = cell_r.add_paragraph()
            p_r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_r2.paragraph_format.space_before = Pt(0)
            p_r2.paragraph_format.space_after = Pt(1)
            r_r2 = p_r2.add_run(right_sub)
            r_r2.font.size = Pt(8.5)
            r_r2.font.color.rgb = RGBColor(100, 116, 139)

    def add_bullet(text, bold_prefix=None, space_after=1.5):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.08
        p.paragraph_format.left_indent = Inches(0.2)
        
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
            r_bold.font.size = Pt(9)
            r_bold.font.color.rgb = RGBColor(15, 23, 42)
        
        run = p.add_run(text)
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # =========================================================================
    # HEADER: NAME & CONTACT
    # =========================================================================
    p_name = add_p(space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_name = p_name.add_run("RONGALI RUPESH")
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(17)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(15, 23, 42)

    p_contact = add_p(space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_c = p_contact.add_run("rupesh72111221@gmail.com   |   +91 93917 25373   |   linkedin.com/in/rupesh-r-84b183311   |   github.com/rupesh12k6")
    r_c.font.size = Pt(9)
    r_c.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # SUMMARY
    # =========================================================================
    add_section_header("Professional Summary")
    p_sum = add_p(space_before=2, space_after=3, line_spacing=1.12)
    p_sum.add_run(
        "Backend-focused Computer Science undergraduate skilled in Java and Spring Boot, with strong foundations in Data Structures, "
        "Algorithms, and Distributed Systems. Built production-style federated platforms (DEPA-compliant consent manager, campus recruitment "
        "portal, anti-spam API) featuring asymmetric cryptography (RS256/ECDH), secure microservices, and real-time Redis caching. "
        "Demonstrated problem-solving capabilities with 750+ DSA problems solved and multiple national coding contest wins."
    )

    # =========================================================================
    # EDUCATION
    # =========================================================================
    add_section_header("Education")
    add_item_header_2col(
        "B.Tech in Computer Science & Engineering",
        "Anil Neerukonda Institute of Technology & Sciences (ANITS), Visakhapatnam",
        "2023 – 2027",
        "CGPA: 9.0 / 10.0"
    )
    add_item_header_2col(
        "Senior Secondary (Class XII), MPC",
        "Sasi Junior College, Visakhapatnam — BIEAP",
        "2023",
        "Score: 97.7%"
    )

    # =========================================================================
    # TECHNICAL SKILLS
    # =========================================================================
    add_section_header("Technical Skills")
    
    def add_skill_line(category, items):
        p = add_p(space_before=0, space_after=1.5, line_spacing=1.08)
        r_cat = p.add_run(category + ": ")
        r_cat.font.bold = True
        r_cat.font.size = Pt(9)
        r_cat.font.color.rgb = RGBColor(15, 23, 42)
        r_items = p.add_run(items)
        r_items.font.size = Pt(9)
        r_items.font.color.rgb = RGBColor(51, 65, 85)

    add_skill_line("Languages", "Java (17+), SQL, C, Python")
    add_skill_line("Backend & Microservices", "Spring Boot, Spring Security, Spring Data JPA, Hibernate, RESTful APIs, JJWT, JDBC")
    add_skill_line("Applied Security & Cryptography", "Asymmetric Signatures (RS256/RSA-2048), ECDH (Secp256r1), AES-128-GCM (AEAD), BCrypt, RBAC")
    add_skill_line("Databases & In-Memory Stores", "PostgreSQL, MySQL, Redis (Sorted Sets, TTL Caching)")
    add_skill_line("System Design & Architecture", "Distributed Systems, Data-Blind Architecture, Rate Limiting, Concurrency Control, Caching")
    add_skill_line("Developer Tools & Platforms", "Git, GitHub, Docker, Postman, Maven, Linux/Bash")

    # =========================================================================
    # PROJECTS
    # =========================================================================
    add_section_header("Technical Projects")

    # Project 1: DEPA Consent Manager
    add_item_header_2col(
        "DEPA Consent Manager & Federated Academic Credential Exchange",
        "github.com/rupesh12k6/DE_9_Infosys",
        "Java 17, Spring Boot, RS256, ECDH, AES-GCM, Postgres, Docker"
    )
    add_bullet("Architected a 3-tier federated consent platform compliant with India’s DEPA & DPDP framework, enabling data-blind, peer-to-peer academic credential exchange between autonomous university nodes.")
    add_bullet("Engineered an asymmetric trust engine using RS256 (RSA-2048) to mint tamper-proof access grant tokens, decoupling verification from database hits and ensuring non-repudiation across institutions.")
    add_bullet("Implemented an end-to-end encrypted transport tunnel using Elliptic Curve Diffie-Hellman (ECDH) key agreement and AES-128-GCM, guaranteeing the central Consent Manager remains strictly data-blind.")
    add_bullet("Built dual-layer verification coupling offline RS256 token validation with real-time synchronous introspection (<150ms), enforcing instant revocation and eliminating stale token abuse.")
    add_bullet("Enforced strict data minimization and RBAC, dynamically filtering and extracting only student-approved attributes (e.g., CGPA vs. transcripts) before encryption.")

    # Project 2: BotShield API
    add_item_header_2col(
        "BotShield API — Anti-Spam Social Media Backend",
        "github.com/rupesh12k6/BotShieldAPI",
        "Java, Spring Boot, PostgreSQL, Redis, REST APIs, Concurrency"
    )
    add_bullet("Engineered an anti-spam social backend separating human users from automated bots via weighted engagement algorithms (+50 humans / +1 bots) to prioritize genuine content.")
    add_bullet("Implemented a bot cooldown system preventing automated reply-spam for 15-minute intervals using Redis key expiration (TTL).")
    add_bullet("Developed a real-time leaderboard using Redis Sorted Sets updated atomically on engagement, eliminating heavy repeated database count queries.")
    add_bullet("Designed threaded comments supporting depth limits of 20 with concurrent lock handling for duplicate likes and null edge-cases.")

    # Project 3: DriveFlow
    add_item_header_2col(
        "DriveFlow — Campus Recruitment Platform",
        "github.com/rupesh12k6/DriveFlow_backend  |  drive-flow-eight.vercel.app",
        "Spring Boot, Spring Security, JWT, PostgreSQL, React, Docker"
    )
    add_bullet("Built a multi-tenant recruitment platform supporting 4 distinct roles (Student/Company/Admin/Super Admin) with JWT-based RBAC.")
    add_bullet("Designed 50+ RESTful APIs managing the recruitment drive lifecycle with automated student eligibility filtering and shortlisting.")
    add_bullet("Optimized PostgreSQL queries with composite indexing and keyset pagination, handling large candidate datasets with low latency.")
    add_bullet("Constructed a secure resume-preview streaming pipeline from Cloudinary, enforcing fine-grained tenant isolation for company recruiters.")

    # =========================================================================
    # WORK EXPERIENCE
    # =========================================================================
    add_section_header("Work Experience")
    add_item_header_2col(
        "Java Developer Intern",
        "Ascendix Solutions",
        "May 2025 – June 2025",
        "Visakhapatnam, India"
    )
    add_bullet("Engineered backend database modules using JDBC for high-throughput relational data operations with connection pooling.")
    add_bullet("Developed a real-time Currency Exchange application in Java integrating external live rate feeds from ExchangeRate-API.")
    add_bullet("Built end-to-end Java desktop enterprise tools incorporating transactional integrity and comprehensive exception handling.")

    # =========================================================================
    # AWARDS & COMPETITIVE PROGRAMMING
    # =========================================================================
    add_section_header("Awards & Competitive Programming")
    add_bullet("Secured 1st Prize in TechNova National Coding Contest among participants nationwide.", "National Coding Champion: ")
    add_bullet("Secured 1st Place in Code Velocity Competitive Programming Event.", "1st Place: ")
    add_bullet("Solved 500+ problems on LeetCode and 250+ problems on GeeksforGeeks (Institute Rank 35).", "Competitive Problem Solving: ")
    add_bullet("Software Engineer (HackerRank)  |  Java (HackerRank)  |  SQL and Relational Databases 101 (IBM Skills Network).", "Certifications: ")

    doc.save(output_path)
    print(f"Successfully generated optimized resume at: {output_path}")

if __name__ == '__main__':
    create_resume_docx('reports/Rongali_Rupesh_Resume.docx')

