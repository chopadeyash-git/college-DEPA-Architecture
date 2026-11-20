import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for j, cell in enumerate(row.cells):
                set_cell_background(cell, "1F4E78") # Deep Navy
                set_cell_margins(cell, top=110, bottom=110, left=130, right=130)
                cell.width = col_widths[j]
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        run.font.name = 'Calibri'
                        run.font.size = Pt(10)
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
        else:
            bg_color = "F2F5F9" if i % 2 == 1 else "FFFFFF"
            for j, cell in enumerate(row.cells):
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=85, bottom=85, left=130, right=130)
                cell.width = col_widths[j]
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        run.font.name = 'Calibri'
                        run.font.size = Pt(9.5)

def build_final_report_document(output_path):
    doc = docx.Document()
    
    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base style
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 41, 59)

    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 120)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = RGBColor(100, 116, 139)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 120)
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(30, 41, 59)
        run = p.add_run(text)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(30, 41, 59)
        run = p.add_run(text)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_code_block(code_text, title=None):
        if title:
            p_title = doc.add_paragraph()
            p_title.paragraph_format.space_before = Pt(6)
            p_title.paragraph_format.space_after = Pt(2)
            p_title.paragraph_format.keep_with_next = True
            r_t = p_title.add_run(title)
            r_t.font.name = 'Calibri'
            r_t.font.size = Pt(10)
            r_t.font.bold = True
            r_t.font.color.rgb = RGBColor(71, 85, 105)

        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F8FAFC") # Light slate background
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="3B82F6"/>' # Blue left highlight
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(15, 23, 42)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # DOCUMENT CONTENT (TECHNICAL-FIRST FORMAT)
    # =========================================================================

    add_title("Institutional Onboarding & Federation Prerequisites")
    add_subtitle("DEPA Academic Credential Trust & Consent Network — Technical Specification")

    # 1. System Scope
    add_h1("1. Architectural Scope & Operating Principles")
    add_p(
        "Under the India Data Empowerment and Protection Architecture (DEPA), the Consent Manager (CM) operates strictly as an "
        "authoritative trust anchor and consent fiduciary. Participating universities function as autonomous Data Providers (Holders) "
        "or Data Consumers (Requesters). The architecture enforces two foundational guarantees:"
    )
    add_bullet(" Student academic records (CGPA, transcripts, degrees) remain in the exclusive custody of the university and are never stored, proxied, or seen by the Consent Manager.", "Data-Blind Fiduciary:")
    add_bullet(" Data transfers occur directly peer-to-peer using ephemeral ECDH key agreement and AES-128-GCM authenticated payload encryption.", "End-to-End Cryptographic Tunnel:")

    # 2. Onboarding Lifecycle
    add_h1("2. Institutional Onboarding Lifecycle & Gating Table")
    add_p("A college transitions through an explicit 8-stage zero-trust lifecycle before being admitted to active federation:")

    t0_data = [
        ["Stage", "Action & Procedure", "Enforced Exit Condition"],
        ["1. Application", "College submits institution profile, role (Provider/Consumer), and authorized contact details.", "Application dossier accepted and registered in CM audit queue."],
        ["2. Due Diligence", "CM administrator verifies institutional charter, accredited domain, and privacy policies.", "Administrative approval recorded by authorized reviewer."],
        ["3. CM Registration", "CM Super Admin initiates registration via POST /api/admin/organizations.", "College entity created in PENDING status with unique organizationCode."],
        ["4. Provisioning", "CM provisions named Org Admin account, issues machine API key, and stores public key.", "College admin can authenticate; key material bound to organization."],
        ["5. Integration Testing", "Automated execution of 10-step full-system verification suite across all nodes.", "Token verification, data minimization, and live revocation checks pass."],
        ["6. Security Audit", "Validation of endpoint reachability, absence of plain-text secrets, and CORS boundaries.", "Technical readiness checklist fully satisfied and signed off."],
        ["7. Activation Gate", "CM Super Admin calls PATCH /api/admin/organizations/{id}/activate.", "Status set to ACTIVE; federation security filters permit live traffic."],
        ["8. Federation", "Continuous monitoring of service health, audit logging, and cryptographic key rotation.", "Operational compliance maintained; inactive or revoked nodes blocked."]
    ]
    t0 = doc.add_table(rows=len(t0_data), cols=3)
    for r_idx, row in enumerate(t0_data):
        for c_idx, val in enumerate(row):
            t0.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t0, [Inches(1.3), Inches(3.2), Inches(2.5)])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 3. Technical Prerequisites Checklist
    add_h1("3. Technical Prerequisites & Verification Checklist")
    add_p("To successfully pass the activation gate, the college node must satisfy the following technical criteria:")
    add_bullet(" Unique organization code (e.g., COLLEGE_A, COLLEGE_B) registered with unique database constraint.", "Unique Federation Identity:")
    add_bullet(" Highly available REST endpoints for login, data onboarding, and data access (e.g., http://localhost:8081).", "Resolved Service Endpoints:")
    add_bullet(" Generation and registration of an RSA-2048 Public Key (X.509 PEM); matching Private Key retained locally.", "Asymmetric Public Key:")
    add_bullet(" Provider node validates CM RS256 token signatures and queries GET /api/access-grants/{id}/validate live.", "Real-Time Introspection:")
    add_bullet(" Provider extracts strictly the approved field scopes (e.g., CGPA), discarding unapproved attributes.", "Granular Data Minimization:")
    add_bullet(" Transcripts transfer directly peer-to-peer using ECDH (Secp256r1) key agreement and AES-128-GCM cipher.", "Payload Transport Encryption:")

    # 4. Federation API Endpoints Directory
    add_h1("4. Federation API Endpoint Directory & Security Controls")
    add_p("The table below details the active API routes, role-based access controls (RBAC), and cryptographic guards across nodes:")

    t_api_data = [
        ["Service Node", "HTTP Method & Route", "Auth / Role Guard", "Cryptographic / Security Mechanism"],
        ["Consent Manager", "POST /api/admin/organizations", "Bearer JWT (SUPER_ADMIN)", "Admin-mediated onboarding; validates uniqueness of organizationCode; creates in PENDING status."],
        ["Consent Manager", "PATCH /api/admin/organizations/{id}/activate", "Bearer JWT (SUPER_ADMIN)", "Human approval gate; changes status to ACTIVE; unblocks federation participation."],
        ["Consent Manager", "POST /api/admin/organizations/{id}/org-admin", "Bearer JWT (SUPER_ADMIN)", "Provisions institutional administrator; credentials hashed using BCrypt (work factor 10)."],
        ["Consent Manager", "GET /api/access-grants/public-key?kid={kid}", "Public / Unrestricted", "Exports CM's RSA-2048 public key in X.509 PEM format; supports kid parameter for key rotation."],
        ["Consent Manager", "POST /api/data-requests", "Bearer JWT (ORG_ADMIN)", "Issues academic credential inquiry bound to requesting consumer and target provider organizations."],
        ["Consent Manager", "POST /api/consents/{id}/approve", "Bearer JWT (STUDENT)", "Student granular approval; mints RS256-signed Access Grant JWT using CM's persistent private key."],
        ["Consent Manager", "GET /api/access-grants/{id}/validate", "Federation Node Call", "Real-time synchronous introspection; verifies active grant status and detects immediate student revocation."],
        ["College A (Provider)", "POST /api/data/access/{grantId}", "Bearer JWT (CM Grant)", "Validates CM RS256 signature, executes live CM introspection, filters approved fields, and negotiates ECDH."],
        ["College B (Consumer)", "POST /api/consumer/fetch-direct-data", "Internal Key (X-API-KEY)", "Consumer initiation; pins provider URL, initiates ECDH 256-bit key agreement, and decrypts AES-GCM."]
    ]
    t_api = doc.add_table(rows=len(t_api_data), cols=4)
    for r_idx, row in enumerate(t_api_data):
        for c_idx, val in enumerate(row):
            t_api.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_api, [Inches(1.2), Inches(2.2), Inches(1.5), Inches(2.1)])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 5. Cryptographic Profile Specification
    add_h1("5. Cryptographic Algorithm & Key Lifecycle Specification")
    add_p("Standardized cryptographic algorithms implemented across the DEPA network:")

    t_crypto_data = [
        ["Security Layer", "Algorithm & Parameters", "Key Custody & Storage", "Operational Function in DEPA"],
        ["DEPA Access Grant Signing", "RS256 (RSA-2048 / SHA-256)", "CM Private Key strictly retained on CM server; Public Key published as X.509 PEM.", "Signs tamper-proof access tokens containing grantId, studentId, purpose, and approved field scopes."],
        ["College Identity Assertion", "RS256 (RSA-2048 / SHA-256)", "College Private Key stored locally under ./keys; Public Key registered with CM.", "Signs short-lived student identity assertions during decentralized portal authentication."],
        ["Peer Key Agreement", "ECDH (Secp256r1 / P-256 curve)", "Ephemeral key pair generated per transfer; discarded immediately after session.", "Generates 128-bit shared secret peer-to-peer without transmitting secret over the wire (Data-Blindness)."],
        ["Payload Transport Cipher", "AES-128-GCM (AES/GCM/NoPadding)", "Derived from ECDH shared secret; fresh 12-byte random IV per transaction.", "Authenticated Encryption (AEAD): encrypts student records with 128-bit GMAC anti-tampering verification tag."],
        ["Credential Protection", "BCrypt (Cost Factor 10, 128-bit Salt)", "One-way password digest stored in PostgreSQL users and admins tables.", "Protects stored administrator and student passwords against offline dictionary and rainbow-table attacks."],
        ["Web Session Token", "HMAC-SHA512 (HS512)", "256/512-bit symmetric secret managed in environment configuration.", "Lightweight, stateless authentication for active portal sessions across admin and student dashboards."]
    ]
    t_crypto = doc.add_table(rows=len(t_crypto_data), cols=4)
    for r_idx, row in enumerate(t_crypto_data):
        for c_idx, val in enumerate(row):
            t_crypto.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    style_table(t_crypto, [Inches(1.3), Inches(1.8), Inches(1.8), Inches(2.1)])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 6. Concrete API Contracts & Payloads (The Engineering Proof)
    add_h1("6. Production API Schemas & Cryptographic Payloads")
    add_p("Representative JSON request and response payloads executed during live inter-college credential exchange:")

    # 6.1 Organization Registration Payload
    add_code_block(
"""// POST /api/admin/organizations (Request)
{
  "organizationCode": "COLLEGE_A",
  "name": "College A University",
  "email": "contact@collegea.edu",
  "dataBaseUrl": "http://localhost:8081",
  "loginEndpoint": "http://localhost:3002",
  "publicKey": "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0r7...\\n-----END PUBLIC KEY-----",
  "status": "PENDING"
}

// Response (HTTP 201 Created)
{
  "organizationId": "ORG_9F4B21A0",
  "organizationCode": "COLLEGE_A",
  "status": "PENDING",
  "createdAt": "2026-11-06T10:30:00Z"
}""",
        title="Listing 6.1: College Registration Payload (Admin-Mediated Onboarding)"
    )

    # 6.2 Data Access Grant Token
    add_code_block(
"""// Decoded RS256 Bearer Access Token (Minted by Consent Manager)
Header:
{
  "alg": "RS256",
  "kid": "CM_9A4F2C1B",
  "typ": "JWT"
}
Payload Claims:
{
  "iss": "consent-manager",
  "sub": "COLLEGE_B",
  "aud": "COLLEGE_A",
  "grant_id": "GRNT_A812C4",
  "data_principal_id": "STU-2023-001",
  "purpose": "Master's Degree Academic Evaluation",
  "scope": ["CGPA", "TRANSCRIPT", "DEGREE_CERTIFICATE"],
  "iat": 1790688000,
  "exp": 1790774400
}""",
        title="Listing 6.2: DEPA Access Grant Token Schema (Asymmetric RS256 Signed)"
    )

    # 6.3 P2P Encrypted Data Transfer Payload
    add_code_block(
"""// Step 1: POST /api/data/access/GRNT_A812C4 (College B Request to College A)
Headers:
  Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkNNX...
Payload:
{
  "consumerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9xZ2Q+8w...[Base64 Secp256r1 Key]"
}

// Step 2: Response from College A (HTTP 200 OK)
{
  "providerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAER5v9N3...[Base64 Secp256r1 Key]",
  "encryptedData": "w7rLq3N8Z9...[Base64 AES-128-GCM: 12-byte IV + Ciphertext + 128-bit GMAC Tag]"
}

// Step 3: Decrypted Payload in College B Memory (Data Minimization Enforced)
{
  "STUDENT_ID": "STU-2023-001",
  "FULL_NAME": "Alice Sharma",
  "CGPA": "9.42",
  "DEGREE_CERTIFICATE": "Bachelor of Technology in Computer Science",
  "TRANSCRIPT": "Completed 8 Semesters with Grade A Distinction"
}""",
        title="Listing 6.3: Peer-to-Peer Encrypted Data Exchange (ECDH + AES-128-GCM)"
    )

    # Save
    doc.save(output_path)
    print(f"Successfully generated final report document at: {output_path}")

if __name__ == '__main__':
    build_final_report_document('reports/Prerequisites_CM_Final.docx')
