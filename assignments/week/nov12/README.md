## week/nov12

- Configured macOS zsh PATH (`~/.local/bin/code`) to launch multiple isolated VS Code instances directly from terminal via `code .` (Post #185).
- Converted all class repositories in `~/work/` (`sugwu123`, `cloudmesh-ai-vm`, `cloudmesh-ai-vm-results`, `cloudmesh-ai-common`, `cloudmesh-ai-llm-mock`) to SSH remotes (`git@github.com:...`) and verified passphrase-protected Ed25519 SSH key authentication (`Hi Sugwu123! You've successfully authenticated`) loaded into macOS Keychain `ssh-agent` (Post #185 & Post #188).
- Verified Piazza real-time and auto-follow notification settings and completed Post #187 and Post #189 confirmations.
- Connected VS Code Cline (`OpenAI Compatible` provider) to Jetstream2 LLM (`https://llm.jetstream-cloud.org/api`, model `gemma-4-31b-it`) with restricted local credentials (`~/.config/jetstream/env`, `chmod 600`).
- Evaluated `SPORTSSTATS` FastAPI/Pydantic endpoints and `cloudmesh-ai-vm` (`dev3`) tasks using Plan/Act verification workflow and 34-test regression suite (`make test`).

### Enabling `code .` from macOS Terminal (Post #185d)
- **Why `code .` failed initially:** Installing Visual Studio Code into `/Applications/Visual Studio Code.app` on macOS does not automatically add its internal CLI binary (`Contents/Resources/app/bin/code`) to `/usr/local/bin` or the user's `zsh` `PATH`.
- **How it was resolved:** Linked `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code` into `~/.local/bin/code` and exported `PATH="$HOME/.local/bin:$PATH"` in `~/.zshrc`, allowing multiple independent VS Code sessions to be launched from separate terminal directories with `code .`.
