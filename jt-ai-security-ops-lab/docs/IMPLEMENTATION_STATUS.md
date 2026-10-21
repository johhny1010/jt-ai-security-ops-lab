# Implementation Status — Evidence-Based

**Scope:** historical project observations from October 2026. This is not a live availability page or release certification.

| Component | Evidence status | Qualification |
|---|---|---|
| OPNsense management TLS/CA | Verified in terminal | Certificate verified; HTTPS returned 200 using supplied public CA |
| Six firewall read endpoints | Verified in terminal | 6/6 responses successful during test; counts fluctuate |
| Linux observer systemd service | Verified in terminal | Timer/service status success in prior tests |
| Three SSH remote collectors | Verified in snapshot | Remote host status was `ok` at observation time |
| Ollama native tool-call response | Verified in terminal | Model emitted structured gateway tool call, execution separate |
| Telegram SOC policy and evidence bridge | Installed and running at test | Does not guarantee correct interpretation of data |
| Deterministic inventory router | Installed and response observed | Correctly caveated ARP/DHCP, still had broader workflow limitations |
| Admin broker process | Verified as active | Dedicated root-owned broker connectivity probe passed |
| Host-alias change proposal | Observed in Telegram | Approval code and pending action generated |
| Host-alias cancellation | Observed in Telegram | Cancellation was acknowledged |
| Successful OPNsense state mutation | **Not verified** | No confirmed applied write/readback test recorded |
| Full NAT/DHCP/VLAN/firewall rule write coverage | **Not implemented in recorded project** | Roadmap work |
| PhD-level accuracy / no hallucinations | **Not claimed** | Strong prompt alone is insufficient |
| Full autonomous root-cause remediation | **Not verified** | Bounded read-tool loop test reported successful |

## Public demonstration status

- Synthetic fixture and schema-based read tools: implemented, tested locally.
- Offline tool chain: implemented, tested locally.
- Optional local Ollama tool loop: included as an illustrative connector; requires user-installed model, not tested by public CI.
- Approval simulator: in-memory and nonprivileged; tested; **not** a production approval identity service.
- CI tests/safety scan: run on every proposed change through GitHub Actions when enabled.
