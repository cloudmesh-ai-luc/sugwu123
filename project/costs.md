# Appendix: Costs and Open Alternatives

Estimates were checked against official sources on October 15, 2026. They are planning estimates, not evidence of active credits or a bill already incurred.

| Component | Current use or estimate | Free/open alternative |
| --- | --- | --- |
| Sports application | Python standard library, SQLite, HTML/JS; no application API fee | Already open tooling; runs locally |
| Historical data | FiveThirtyEight NBA data under CC BY 4.0; no data purchase | Existing synthetic fixture for software checks; cannot establish real predictive accuracy |
| Multipass | Local CPU, RAM, disk, electricity; no provider VM bill | Direct host execution; Multipass is open source |
| Chameleon KVM@TACC | Depends on approved allocation and quota; allocation not verified | Multipass for local reproduction; remote portability remains unproven |
| Google Compute Engine | Short e2-micro CPU run; account, region, quota, and billing unverified | Multipass or eligible Chameleon allocation |
| Google AI Pro | Public U.S. listing: $19.99/month before taxes; $10/month GenAI/Cloud credit listed through Developer Program benefits | No paid plan needed for this application; appropriately licensed local models may help writing |
| OpenAI Codex development help | Used for preparation; subscription price and attributable task cost unavailable | Manual coding/review, course documentation, or a suitably licensed local code model |

## Worked Google Estimate

The official Iowa (`us-central1`) on-demand e2-micro listing is **$0.008376428 per VM-hour**. A 15-minute run costs about **$0.00209 in compute** at that rate: `0.25 × 0.008376428`. This is not a full invoice estimate. Persistent disks, external IPv4, network transfer, taxes, regional differences, and other resources can add charges. An e2-micro has 1 GiB memory and shared CPU; application suitability and image compatibility require a real test.

The free tier lists one eligible e2-micro instance's monthly usage in selected U.S. regions with additional limits. Eligible new accounts may receive a $300, 90-day trial. Neither free-tier eligibility nor trial availability has been confirmed for this account. Google AI Pro's listed $10 monthly credit requires the applicable benefit/account setup; it is not assumed to be claimed, attached to this billing account, or applicable to every service.

Before a paid run, the operator must verify billing, credit terms and region, configure a low budget alert, restrict quota, and keep the run short. A budget alert does not stop spending. After collecting results, remove the dedicated VM and unneeded disks, addresses and other resources, then check inventory and billing. No paid project upgrade or purchase was performed during this preparation.

## Service Choice

The current model is small CPU-only logistic regression. Neither a GPU nor a hosted LLM is needed for inference. An external commercial sports API or paid explanation service adds no necessary capability to this milestone. Open local tools preserve reproducibility without a subscription. A later LLM feature would need a separate cost, license, data-handling, and accuracy evaluation.

## Sources

- [Google Developer Program plans and pricing](https://developers.google.com/program/plans-and-pricing)
- [Compute Engine general-purpose VM pricing](https://cloud.google.com/products/compute/pricing/general-purpose)
- [Google Cloud free program and trial limits](https://docs.cloud.google.com/free/docs/free-cloud-features)
- [FiveThirtyEight data license](https://github.com/fivethirtyeight/data#license)
- [Multipass source and license](https://github.com/canonical/multipass)

Acknowledgment: OpenAI Codex researched and drafted this appendix. Prices are public listings rather than verified account-specific entitlements or charges.
