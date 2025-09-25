
# Security & Compliance
The importance of rising security to protect health-related data is more crucial than ever, The HIPAA Security Guidance modified the Health Insurance Portability and Accountability Act of 1996 (HIPAA) Security Rule to strengthen cybersecurity protections for electronic protected health information (ePHI). This represents the first major update to be made in two decades, demonstrating urgent threat as a result of the increasing frequency and severity of healthcare cyberattacks.

## HIPAA Security Rule
HIPAA Security guidance refers to a comprehensive framework established by the Health Insurance Portability and Accountability Act (HIPAA) Security Rule to protect electronic protected health information (ePHI). The current ruling requires physicians to provide appropriate administrative, physical, and technical safeguards to ensure the confidentiality, integrity, and security of electronic protected health information.

- **Administrative Safeguards**: Include policies, procedures, and risk analysis requirements
- **Physical Safeguards**: Protect computer systems, equipment, and facilities housing ePHI
- **Technical Safeguards**: Technical safeguards concern the technologies that store and access ePHI. These can include access control and monitoring, multi-factor authentication, encryption, firewalls, device management, and endpoint security.

## SMART Implementation
In the software applications of systems like FHIR, HL7 (Health Level Seven) also defined their own implementation guide to provide the technical safeguards necessary to ensure safety while healthcare providers exchange, integrate, and share electronic health information. This was defined using SMART implementation to authorize, authenticate, and integrate FHIR-based data systems which is based on OAuth2.0 for client applications (i.e. limited accessibility).

### SMART Authorization
- **App Launch**: In cases of smart mobile applications or interfaces which allow users to connect with FHIR servers to retrieve their relevant data. This system allow only the current selected patient (usually the owner of their data) to be shared with the app. Authorization allows for delegation of a user’s permissions to the app itself.

- **Backend Services**: Authorizing a specific backend server to be allowed to contact the FHIR server, when there is no user directly involved in the launch process.

### SMART Authentication
Authentication is required to double check that that client is who's claiming to be.

- **Asymmetric ("Private Key JWT") Authentication**: In this type of authentication, the client signs a JWT with their private key and the server verifies with the public key. This is safe as it's scalable. One key could authorize multiple secrets and it works very well for distributed systems.
- **Symmetric ("Client Secret") Authentication**: Which is a pre-established secret between the client and the server. It works when the client demonstrates knowledge of the secret. If the secret is compromised, both parties are affected, so it's hard rotate and manage it at scale.


## Data Privacy & Audit Logging
This is within the scope of protecting ePHI beyond secure transmission and storage as it requires accountability and traceability, which is done through the following:

- **Encryption**: All ePHI must be encrypted both at rest and transmission (of packets).
- **De-identification**: When data is used for research, testing, or analytics, identifiers should be removed or masked (which is standard in sensitive data).
- **Audit Logging**: Every access or modification of FHIR resources should be logged.
- **Log Integrity**: Logs should be immutable (append-only) and stored separately from the application database.

## Role-Based Access Control (RBAC)
This is HIPAA’s “minimum necessary” standard which requires restricting access to only what users need. SMART defines this as scope to define specific access permissions that can be delegated to a client application based on your role (client/server) or (clinician/adminstrator/researcher).

