# Appendix: SPORTSSTATS Costs and Open Alternatives

Checked October 15, 2026. The account screen and launch price are observations from that morning. The worked estimate is not an actual bill.

| Component | Current use or estimate | Free/open alternative |
| --- | --- | --- |
| Application | Python standard library, SQLite, HTML/JS; no paid application API | Run the same code locally |
| Historical data | FiveThirtyEight NBA data, CC BY 4.0; no purchase | Separate synthetic fixture for software checks |
| Multipass | Local CPU, RAM, disk, electricity; no provider VM bill | Direct host execution; Multipass is open source |
| Chameleon KVM@TACC | Needs an approved allocation and quota; access unverified | Local Multipass; remote portability still needs testing |
| Amazon EC2 | Selected public cloud; t3.micro in Ohio, Ubuntu 24.04, 8 GiB disk | Local Multipass or an eligible Chameleon allocation |
| OpenAI Codex development help | Used substantially; subscription price and this task's share of cost unavailable | Manual coding/review, course materials, or an appropriately licensed local code model |

## AWS Account and Worked Estimate

The student's AWS account screen showed **Free plan, $100 credits remaining, 183 days remaining**, with April 15, 2027 shown as the end date. This was observed on October 15 at about 8:48 am Chicago time. AWS states that its Free plan ends after six months or when credits run out, whichever happens first. The balance and terms must be checked again before use. No paid-plan upgrade was performed during this preparation.

The Ohio (`us-east-2`) launch screen displayed a Linux t3.micro compute rate of **$0.0104/hour**. A 15-minute run at that rate is **$0.0026 in compute**: `0.25 × 0.0104`. This is a planning calculation before applying credits. It excludes EBS storage, public IPv4, data transfer, possible surplus CPU credits, taxes, and other resources. The selected instance has 2 virtual CPUs and 1 GiB RAM. The application later passed 34 guest tests and displayed the historical NBA dashboard on this instance.

A running EC2 instance, SSH access, guest tests, and the deployed dashboard were confirmed in the afternoon screenshots. Actual charges and the current credit balance have not been checked. Google Cloud was considered earlier but is no longer the selected public cloud. Neither Google AI Pro nor a paid sports-data service is needed for this application.

## Cost Controls

Use one small instance and a short test. Check the Free-plan balance and available usage alerts. A budget alert alone does not stop spending. Stopping a VM can leave storage and other billable resources behind. After preserving the needed results, remove the dedicated VM and unneeded disks or addresses, then check inventory and billing. Keep the account on its Free plan unless a separate decision is made to upgrade.

The course guidelines require billing alarms on commercial cloud accounts. No configured AWS billing alarm has been observed yet; Free-plan credits do not complete that requirement. On OpenStack, use Chameleon KVM@TACC and the smallest suitable VM. Shelve or delete it when idle; stopping alone is not sufficient under the assignment's resource rule.

## Why These Services

The model is a small CPU-only classifier. It needs no GPU or hosted LLM. Local Python and SQLite keep the analysis reproducible without a subscription. The remote clouds are used to test deployment and repeat the same calculation, not to change the model's accuracy.

## Sources

- [AWS Free Tier FAQ and current plan terms](https://aws.amazon.com/free/free-tier-faqs/)
- [EC2 on-demand pricing and additional charges](https://aws.amazon.com/ec2/pricing/on-demand/)
- [EBS pricing](https://aws.amazon.com/ebs/pricing/)
- [FiveThirtyEight data license](https://github.com/fivethirtyeight/data#license)
- [Multipass source and license](https://github.com/canonical/multipass)

Acknowledgment: OpenAI Codex researched and drafted this appendix. Account observations, estimates, and unverified charges are stated separately. Student review is still needed.
