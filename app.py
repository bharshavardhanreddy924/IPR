from flask import Flask, render_template, request # Added request for active nav link
import os
from pathlib import Path
app = Flask(__name__)

# --- Helper Functions for Content Generation ---
def create_list_html(items, list_type="ul", item_class=None, list_class=None, bold_first=False):
    li_tags = ""
    for item in items:
        class_attr = f' class="{item_class}"' if item_class else ''
        if isinstance(item, tuple):  # For (title, description)
            li_tags += f"<li{class_attr}><strong>{item[0]}</strong>: {item[1]}</li>"
        else:
            li_tags += f"<li{class_attr}>{item}</li>"

    list_class_attr = f' class="{list_class}"' if list_class else ''
    return f"<{list_type}{list_class_attr}>{li_tags}</{list_type}>"

def create_pros_cons_html(pros, cons):
    pros_html = "<div><h3><span class='section-icon'>👍</span>Pros for Startups</h3>" + create_list_html(pros, item_class="pro") + "</div>"
    cons_html = "<div><h3><span class='section-icon'>👎</span>Cons for Startups</h3>" + create_list_html(cons, item_class="con") + "</div>"
    return f"<div class='pros-cons'>{pros_html}{cons_html}</div>"

def create_code_example_html(code_content, language="text", caption=None):
    caption_html = f"<p><em>Example: {caption}</em></p>" if caption else ""
    return f"{caption_html}<div class='code-block'><pre><code class='language-{language}'>{code_content}</code></pre></div>"

# --- Content for AI Tool Pages (Startup Focused) ---
tools_data = {
    "bard": {
    "name": "Cursor AI",
    "startup_tagline": "The AI-first code editor, designed to help you build software faster with a powerful, integrated AI.",
    "logo_url": "/static/img/cursor-logo.jpeg",
    "official_link": "https://cursor.sh/",
    "cta_link": "https://cursor.sh/",
    "cta_text": "Download Cursor",
    "sections": {
        "intro_startup": "Why Cursor AI for Startup Development?",
        "features_startup": "Key Cursor AI Features for Engineering Teams",
        "getting_started_startup": "Getting Started with Cursor (AI Code Editor)",
        "use_cases_startup": "Cursor in Action: Accelerating Startup Development",
        "integration_startup": "Integrating Cursor into Your Development Workflow",
        "roi_startup": "Cursor AI's ROI: Development Velocity & Code Quality",
        "pricing_startup": "Cursor AI Pricing: Free & Pro Tiers for Startups",
        "action_steps": "Your First Week with Cursor AI: Quick Wins",
        "pros_cons_startup": "Cursor AI: Pros & Cons for Startups",
        "resources_startup": "Further Learning & Cursor Community"
    },
    "content": {
        "intro_startup": """
            <p>Cursor is a code editor built from the ground up for AI-powered development. It's a fork of VS Code, meaning it retains the familiar interface and extensive extension ecosystem that developers love, but with AI capabilities deeply integrated into its core. This is not just a plugin like GitHub Copilot; it's a cohesive environment where the AI has full context of your entire codebase.</p>
            <p>For a startup's engineering team, this means:</p>
            <ul>
                <li><strong>Accelerated Development:</strong> Generate boilerplate code, entire functions, and even complex algorithms in seconds.</li>
                <li><strong>Deeper Code Comprehension:</strong> Instantly understand complex or legacy codebases by asking the AI to explain specific sections.</li>
                <li><strong>Faster Debugging:</strong> Feed error messages directly to the AI, which can scan your code to find the root cause and suggest a fix.</li>
                <li><strong>Efficient Refactoring:</strong> Highlight code and ask the AI to refactor it for readability, performance, or to fit a new pattern.</li>
            </ul>
            <p>Think of it as pair programming with an AI that has perfect memory of your project, knows best practices, and is available 24/7. It significantly reduces the friction of modern software development.</p>
        """,
        "features_startup": create_list_html([
            ("Code-Aware AI Chat", "Chat with an AI that has the full context of your project files. Ask questions, get explanations, and generate code snippets relevant to your work."),
            ("Inline AI Editing (Ctrl/Cmd + K)", "Highlight any block of code and use a natural language prompt to edit or refactor it in place."),
            ("Generate from Scratch", "Prompt the AI to generate new files or large blocks of code based on a description of the desired functionality."),
            ("AI-Powered Debugging", "Paste an error message or select buggy code and have the AI automatically identify the issue and propose a solution."),
            ("Codebase-wide Answers", "Ask questions like 'How does our authentication work?' and get an answer synthesized from across your entire repository."),
            ("VS Code Fork & Extension Compatibility", "Use your favorite themes, keybindings, and most extensions from the VS Code marketplace in a familiar environment."),
            ("Auto-generated Tests & Docs", "Highlight a function and ask the AI to generate corresponding unit tests or documentation strings.")
        ], list_class="key-feature-list", bold_first=True),
        "getting_started_startup": """
            <p>Onboarding your engineering team to Cursor:</p>
            <ol>
                <li><strong>Download and Install:</strong> Head to <a href="https://cursor.sh/" target="_blank">cursor.sh</a> and download the editor for your OS (macOS, Windows, Linux).</li>
                <li><strong>Open a Project:</strong> Launch Cursor and open an existing project folder just like you would with VS Code. It will feel instantly familiar.</li>
                <li><strong>Learn the Core Commands:</strong>
                    <ul>
                        <li><strong>AI Chat:</strong> Press `Cmd/Ctrl + L` to open the chat pane. Ask a question about your code.</li>
                        <li><strong>Inline Edit:</strong> Select a piece of code and press `Cmd/Ctrl + K`. A prompt will appear allowing you to ask for a change.</li>
                    </ul>
                </li>
                <li><strong>Import VS Code Settings:</strong> Cursor often prompts you to import your settings, keybindings, and extensions from VS Code to make the transition seamless.</li>
                <li><strong>(Optional) Add Your API Key:</strong> In the settings, Pro users can add their own OpenAI API key to get priority access to models and better control over usage.</li>
            </ol>
        """,
        "use_cases_startup": """
            <h4>Feature Development & Prototyping:</h4>
            <ul>
                <li><strong>Scaffolding:</strong> "Generate a new React component named 'UserProfile' with props for name, email, and avatar. Include basic styling with Tailwind CSS."</li>
                <li><strong>API Integration:</strong> "Write a Javascript function that fetches data from the `[API_ENDPOINT]` and handles loading and error states."</li>
            </ul>
            <h4>Debugging & Maintenance:</h4>
            <ul>
                <li><strong>Error Resolution:</strong> "I'm getting this traceback: `[paste error here]`. Scan the relevant files and tell me what's wrong and how to fix it."</li>
                <li><strong>Performance Optimization:</strong> "Review this function and suggest ways to make it more performant."</li>
            </ul>
            <h4>Code Refactoring & Quality:</h4>
            <ul>
                <li><strong>Modernization:</strong> "Convert this class-based React component to a functional component using hooks."</li>
                <li><strong>Readability:</strong> "This function is too complex. Refactor it into smaller, single-responsibility helper functions."</li>
            </ul>
            <h4>Onboarding & Code Exploration:</h4>
            <ul>
                <li><strong>Learning a New Codebase:</strong> "Explain the purpose of the `services/payments.js` file and how it interacts with the User model."</li>
                <li><strong>Writing Documentation:</strong> "Generate a README file for this module, explaining what it does and documenting its public functions."</li>
            </ul>
        """,
        "integration_startup": """
            <p>As a fork of VS Code, Cursor's primary integration is with the developer's existing toolchain. It's designed to be a drop-in replacement, not a peripheral tool.</p>
            <p>Key integration points for a startup's workflow:</p>
            <ul>
                <li><strong>VS Code Ecosystem:</strong> The single most important integration. Most extensions for themes (e.g., Cobalt2, Dracula), linters (ESLint, Prettier), language support (Python, Go), and Docker work out of the box.</li>
                <li><strong>Version Control:</strong> Comes with the same robust Git and GitHub integration as VS Code. You can stage, commit, push, and manage pull requests directly from the editor.</li>
                <li><strong>Terminal:</strong> The integrated terminal works exactly as it does in VS Code, allowing you to run build scripts, start servers, and interact with your system without leaving the editor.</li>
                <li><strong>AI Model APIs:</strong> Integrates directly with OpenAI's models (GPT-3.5, GPT-4, etc.). The Pro plan allows you to "Bring Your Own Key" (BYOK) for more direct control over API usage and access to newer models.</li>
                <li><strong>Project Configurations:</strong> Reads existing project configurations like `.eslintrc`, `prettierrc`, and `tsconfig.json` to enforce team-wide coding standards.</li>
            </ul>
            <p><strong>Startup Advantage:</strong> There is virtually zero friction in adopting Cursor. A developer can download it, import their settings, and be more productive within minutes, using all the tools and workflows they already rely on.</p>
        """,
        "roi_startup": """
            <p>For startups, Cursor's ROI is measured in engineering velocity and efficiency, which directly impacts time-to-market.</p>
            <ul>
                <li><strong>Drastically Reduced Development Time:</strong> Automating the generation of boilerplate, tests, and well-understood logic can cut down feature development time significantly.
                    <ul><li><em>Example:</em> If a developer saves 60 minutes per day on routine coding and debugging, that's over 20 hours saved per month, per developer.</li></ul>
                </li>
                <li><strong>Faster Bug Resolution:</strong> AI-assisted debugging reduces the time spent on troubleshooting, allowing developers to ship fixes faster and focus on new features.</li>
                <li><strong>Accelerated Onboarding:</strong> New hires can become productive faster by using the AI to navigate and understand an unfamiliar codebase. This is a massive advantage for fast-growing teams.</li>
                <li><strong>Improved Code Quality and Consistency:</strong> The AI can help enforce best practices and refactor code, leading to a more maintainable and robust application over time.</li>
                <li><strong>Unlocking Senior Developer Focus:</strong> By handling mundane tasks, Cursor frees up senior engineers to focus on high-level architecture and complex problem-solving.</li>
            </ul>
            <p><strong>Measuring ROI:</strong>
                Track sprint velocity or story points completed before and after adoption.
                Survey developers on their perceived time savings for common tasks (e.g., writing a new API endpoint, debugging an issue).
                Measure the time it takes for a new engineer to make their first significant contribution.
            </p>
        """,
        "pricing_startup": """
            <p>Cursor offers a straightforward pricing model that caters to individual developers and teams, making it accessible for startups.</p>
            <ul>
                <li><strong>Free Plan:</strong>
                    <ul>
                        <li>Includes a limited number of "fast" AI responses per month using powerful models like GPT-4. After the limit, it may use slower models or have rate limits.</li>
                        <li>Access to all core editor features.</li>
                        <li><strong>Best for:</strong> Individual developers trying out the tool, or very light usage within a team.</li>
                    </ul>
                </li>
                <li><strong>Pro Plan:</strong>
                    <ul>
                        <li>Priced per user per month (e.g., ~$20/user/month, with annual discounts).</li>
                        <li>Provides a much larger allowance of fast AI responses.</li>
                        <li>Includes the "Bring Your Own Key" (BYOK) feature, allowing you to use your own OpenAI API key for unlimited usage (you pay OpenAI for what you use).</li>
                        <li>Access to the very latest AI models as they become available.</li>
                        <li><strong>Best for:</strong> Any professional developer or startup engineering team. The productivity gains make this a high-ROI investment.</li>
                    </ul>
                </li>
                <li><strong>Business/Enterprise Plan:</strong>
                    <ul>
                        <li>Custom pricing for larger teams.</li>
                        <li>Offers centralized billing, team management, and enhanced security/privacy features.</li>
                        <li>May offer options for self-hosting or stricter data controls.</li>
                    </ul>
                </li>
            </ul>
            <p><strong>Startup Strategy:</strong>
                Have your entire team try the Free plan for a few days.
                The value is usually immediately obvious. Upgrade the entire engineering team to the Pro plan to maximize velocity. The cost per developer is minimal compared to the salary and the potential productivity gains.
            </p>
            <p>Always check the official <a href="https://cursor.sh/pricing" target="_blank">Cursor pricing page</a> for the most current details and features.</p>
        """,
        "action_steps": create_list_html([
            ("<strong>Day 1: Install & Ask a Question.</strong> Install Cursor and open a project. Open the AI Chat (`Cmd/Ctrl+L`) and ask a question about the file you have open, like 'What is the purpose of this file?'. Focus: Understanding AI context.", ""),
            ("<strong>Day 2: Use Inline Edit (`Ctrl+K`).</strong> Find a function in your code. Highlight it, press `Cmd/Ctrl+K`, and type 'add JSDoc comments to this function'. Watch it generate the documentation. Focus: The core editing workflow.", ""),
            ("<strong>Day 3: Generate a New File.</strong> In the chat, prompt the AI: 'Generate code for a new file named `utils.js` that has a function to debounce user input'. Copy the code into a new file. Focus: Code generation.", ""),
            ("<strong>Day 4-5: Build a Real Feature.</strong> Tackle a small ticket from your backlog using Cursor as your primary tool. Use `Ctrl+K` to refactor, chat to debug errors, and code generation to scaffold new components. Focus: Integrating Cursor into your daily workflow.", "")
        ], list_class="action-steps-list", bold_first=False),
        "pros_cons_startup": create_pros_cons_html(
            pros=[
                ("Massive Productivity Boost: Deeply integrated AI significantly speeds up coding, debugging, and refactoring.", "Familiar VS Code Base: Zero learning curve for the UI, and compatibility with most existing VS Code extensions and settings."),
                ("Superior Code Context: AI's ability to reference the entire codebase leads to more relevant and accurate suggestions than simple autocomplete plugins.", "Accelerates Onboarding: A game-changer for new engineers trying to understand a complex project."),
                ("Active Development: The tool is constantly being updated with new features and better AI model integrations.")
            ],
            cons=[
                ("Resource Intensive: Can use more memory and CPU than a standard VS Code setup, especially during intensive AI operations.", "Dependency on AI Provider: Your workflow is tied to the availability and performance of OpenAI's APIs.", "Subscription Cost: The per-seat cost can add up for a growing engineering team.", "Code Privacy: While there are privacy policies, sending code snippets to a third-party API may be a concern for startups with highly sensitive IP (Business plan may mitigate this)."),
                ("Lags Behind VS Code Releases: As a fork, it may sometimes be a few versions behind the official VS Code release, delaying access to VS Code's newest non-AI features.")
            ]
        ),
        "resources_startup": """
            <ul>
                <li><a href="https://cursor.sh/docs" target="_blank" rel="noopener noreferrer">Cursor Official Docs:</a> The best place to start for features and guides.</li>
                <li><a href="https://discord.gg/cursor" target="_blank" rel="noopener noreferrer">Cursor Discord Community:</a> An active community for asking questions, sharing tips, and getting help.</li>
                <li><a href="https://cursor.sh/changelog" target="_blank" rel="noopener noreferrer">Official Changelog:</a> Keep up with the rapid pace of new features and improvements.</li>
                <li><a href="https://twitter.com/cursor_ide" target="_blank" rel="noopener noreferrer">Cursor on Twitter/X:</a> Follow for news and announcements.</li>
            </ul>
        """
    }
},
    # --- ChatGPT ---
    "chatgpt": {
        "name": "OpenAI ChatGPT",
        "startup_tagline": "The versatile AI powerhouse for content, code, and creative solutions, with options from free to enterprise.",
        "logo_url": "/static/img/chatgpt-logo.png",
        "official_link": "https://chat.openai.com/",
        "cta_link": "https://chat.openai.com/auth/login",
        "cta_text": "Try ChatGPT",
        "sections": {
            "intro_startup": "Why ChatGPT for Your Startup?",
            "features_startup": "Key ChatGPT Features for Startup Success",
            "getting_started_startup": "Getting Started with ChatGPT (Free & Paid)",
            "use_cases_startup": "ChatGPT in Action: Startup Use Cases",
            "integration_startup": "ChatGPT Integrations & Custom GPTs for Startups",
            "roi_startup": "ChatGPT ROI: Value Proposition for Startups",
            "pricing_startup": "ChatGPT Pricing Explained for Startups",
            "action_steps": "Your First Week with ChatGPT: Quick Wins",
            "pros_cons_startup": "ChatGPT: Pros & Cons for Startups",
            "resources_startup": "Further Learning & Support"
        },
        "content": {
             "intro_startup": """
                <p>OpenAI's ChatGPT has become a household name in AI, and for good reason. It offers startups a powerful and adaptable tool for a vast range of tasks, from drafting emails and blog posts to generating code and analyzing data. With different models (GPT-3.5 for free access, GPT-4 for paid tiers), ChatGPT can scale with your startup's needs.</p>
                <p>Startups can leverage ChatGPT to:</p>
                <ul>
                    <li><strong>Supercharge Content Marketing:</strong> Create high-quality articles, social media campaigns, and website copy.</li>
                    <li><strong>Accelerate Software Development:</strong> Generate code snippets, debug, understand APIs, and draft documentation.</li>
                    <li><strong>Enhance Customer Engagement:</strong> Draft personalized customer responses or explore chatbot integrations.</li>
                    <li><strong>Streamline Operations:</strong> Summarize documents, extract key information, and automate reporting tasks.</li>
                    <li><strong>Innovate with Custom Solutions:</strong> Use the API or Custom GPTs (paid) to build AI-powered features into your products or internal tools.</li>
                </ul>
            """,
            "features_startup": create_list_html([
                ("Advanced Language Models (GPT-3.5, GPT-4)", "Access to powerful models capable of nuanced understanding, complex reasoning, and high-quality generation."),
                ("Versatile Text & Code Generation", "From marketing copy and creative writing to functional code in multiple languages."),
                ("Custom GPTs (ChatGPT Plus/Team/Enterprise)", "Create tailored versions of ChatGPT for specific tasks or company knowledge, no coding required."),
                ("Plugins (ChatGPT Plus/Team/Enterprise)", "Extend capabilities by connecting to third-party services for web browsing, data analysis, diagramming, etc."),
                ("DALL·E Image Generation (via GPT-4)", "Create unique images from text prompts for marketing, presentations, or product mockups."),
                ("Advanced Data Analysis (Code Interpreter)", "Upload files (CSVs, PDFs, etc.) and have ChatGPT analyze data, create visualizations, and write code to process it."),
                ("API Access", "For developers to integrate ChatGPT's power into custom applications and workflows.")
            ], list_class="key-feature-list", bold_first=True),
            "getting_started_startup": """
                <p>Onboarding your startup to ChatGPT:</p>
                <ol>
                    <li><strong>Choose Your Plan:</strong>
                        <ul>
                            <li><strong>Free Plan:</strong> Access GPT-3.5. Great for initial experimentation and basic tasks. Sign up at <a href="https://chat.openai.com/" target="_blank">chat.openai.com</a>.</li>
                            <li><strong>ChatGPT Plus/Team:</strong> Subscription-based. Access to GPT-4 (more capable), DALL·E, Advanced Data Analysis, Plugins, Custom GPTs, and higher usage limits. Recommended for startups needing advanced features or higher capacity.</li>
                            <li><strong>ChatGPT Enterprise:</strong> For larger organizations needing enhanced security, admin controls, and unlimited high-speed GPT-4.</li>
                        </ul>
                    </li>
                    <li><strong>Create Accounts:</strong> Team members can sign up individually. For Team/Enterprise, an admin will manage users.</li>
                    <li><strong>Explore the Interface:</strong> Similar to Bard, with a prompt box, conversation history, and model selection (if applicable).</li>
                    <li><strong>Experiment with Prompts:</strong>
                        <ul>
                            <li><strong>Provide Context:</strong> "Act as a [role] for a startup in the [industry] space."</li>
                            <li><strong>Specify Format:</strong> "Give me the answer in a bulleted list / table / JSON format."</li>
                            <li><strong>Iterate:</strong> Refine your prompts based on the responses.</li>
                        </ul>
                    </li>
                    <li><strong>Introduce Advanced Features (Paid Tiers):</strong> If on Plus/Team, guide your team on using Plugins, Custom GPTs, and Advanced Data Analysis.</li>
                </ol>
            """,
            "use_cases_startup": """
                <h4>Marketing & Content:</h4>
                <ul>
                    <li><strong>Blog Post Series:</strong> "Outline a 5-part blog series on 'AI for small business productivity', then draft the first post."</li>
                    <li><strong>A/B Test Copy:</strong> "Generate 3 variations of a Facebook ad headline and body text for our new mobile app."</li>
                    <li><strong>Video Scripts:</strong> "Write a 2-minute explainer video script for our SaaS product's key features."</li>
                </ul>
                <h4>Development & Tech:</h4>
                <ul>
                    <li><strong>API Integration Help:</strong> "Explain how to authenticate with the Stripe API using Python and provide a basic charge creation example."</li>
                    <li><strong>Code Refactoring:</strong> "Can you refactor this JavaScript function to be more efficient? [paste code]"</li>
                    <li><strong>Technical Documentation:</strong> "Draft the 'Getting Started' section for our new API documentation."</li>
                </ul>
                <h4>Business Operations & Strategy:</h4>
                <ul>
                    <li><strong>Investor Pitch Deck Content:</strong> "Help me brainstorm key talking points for the 'Problem' and 'Solution' slides of my investor pitch deck."</li>
                    <li><strong>SWOT Analysis:</strong> "Conduct a SWOT analysis for a startup offering [your product/service]."</li>
                    <li><strong>Customer Feedback Analysis:</strong> (Using Advanced Data Analysis) "Analyze this CSV of customer survey responses and identify the top 3 pain points."</li>
                </ul>
            """,
            "integration_startup": """
                <p>ChatGPT offers several ways for startups to integrate its capabilities:</p>
                <ul>
                    <li><strong>Copy-Paste:</strong> The simplest method for transferring generated content into your documents, emails, or code editors.</li>
                    <li><strong>Plugins (Paid Tiers):</strong> Connect ChatGPT to external tools like Zapier (for broader automation), Wolfram (for computation), Canva (for design), or web browsers (for current information). This dramatically expands its utility for specific tasks.</li>
                    <li><strong>Custom GPTs (Paid Tiers):</strong>
                        <ul>
                            <li>Build specialized AI assistants for your team without coding.</li>
                            <li>Upload company-specific documents to give your Custom GPT relevant knowledge (e.g., a "Support Bot" trained on your FAQs, or a "Brand Voice Writer" trained on your style guide).</li>
                            <li>Can connect to external APIs for dynamic actions.</li>
                        </ul>
                    </li>
                    <li><strong>OpenAI API:</strong> For startups with development resources, the API allows you to embed GPT models directly into your own applications, websites, or internal tools. This offers maximum flexibility for creating custom AI-powered solutions.
                        <ul><li><em>Use Cases:</em> AI-powered customer service bots, automated content generation for your platform, intelligent data analysis tools within your product.</li></ul>
                    </li>
                    <li><strong>Zapier/Make.com Integration (via API or Plugins):</strong> Connect ChatGPT to thousands of other apps to automate workflows like drafting email responses from new leads, summarizing articles and posting to Slack, etc.</li>
                </ul>
            """,
            "roi_startup": """
                <p>The ROI from ChatGPT for startups, especially with paid tiers, can be substantial:</p>
                <ul>
                    <li><strong>Productivity Gains (GPT-4):</strong> GPT-4's superior reasoning and generation quality can lead to even greater time savings than free models for complex tasks.
                        <ul><li><em>Example:</em> A developer using GPT-4 for coding assistance might solve problems 20-30% faster. A marketer might draft high-quality content in half the time.</li></ul>
                    </li>
                    <li><strong>Cost Savings on Specialized Tools/Services:</strong>
                        <ul>
                            <li><strong>Content/Copywriting:</strong> Reduce reliance on expensive freelance writers or agencies for initial drafts.</li>
                            <li><strong>Basic Design:</strong> DALL·E image generation can cover some needs for social media graphics or presentation visuals.</li>
                            <li><strong>Data Analysis:</strong> Advanced Data Analysis can perform tasks that might otherwise require a data analyst or specialized software.</li>
                        </ul>
                    </li>
                    <li><strong>Faster Time-to-Market:</strong> Accelerate product development cycles with AI-assisted coding, testing, and documentation. Launch marketing campaigns faster with rapid content creation.</li>
                    <li><strong>Innovation & New Revenue Streams (API/Custom GPTs):</strong> Building AI features into your product can create new value for customers and differentiate your offering, potentially leading to increased sales or new pricing tiers.</li>
                    <li><strong>Improved Decision Making:</strong> Quickly analyze data or research market trends to make more informed strategic choices.</li>
                </ul>
                <p><strong>Tracking ROI (Paid Tiers):</strong> Monitor the cost of ChatGPT subscriptions against time saved (calculated by hourly rates), costs avoided (e.g., freelance fees), and any new revenue generated from AI-powered features or faster GTM.</p>
            """,
            "pricing_startup": """
                <p>OpenAI offers several tiers for ChatGPT, catering to different startup needs:</p>
                <ul>
                    <li><strong>Free Plan:</strong>
                        <ul>
                            <li>Access to GPT-3.5 model.</li>
                            <li>Standard response speed, regular model updates.</li>
                            <li><strong>Best for:</strong> Individual experimentation, basic content drafting, learning prompt engineering. Excellent for very early-stage startups with minimal budget.</li>
                        </ul>
                    </li>
                    <li><strong>ChatGPT Plus (Individual User):</strong>
                        <ul>
                            <li>Around $20/month per user.</li>
                            <li>Access to GPT-4 (more capable, faster, longer context).</li>
                            <li>Access to DALL·E, Advanced Data Analysis, Plugins, Custom GPTs.</li>
                            <li>Higher message limits and faster response times.</li>
                            <li><strong>Best for:</strong> Founders, key team members, or any individual needing maximum AI power and features for daily work. High ROI for power users.</li>
                        </ul>
                    </li>
                    <li><strong>ChatGPT Team:</strong>
                        <ul>
                            <li>Priced per user per month (e.g., $25-$30/user/month, billed annually or monthly). Minimum user count may apply.</li>
                            <li>Includes all Plus features.</li>
                            <li>Admin console for workspace management.</li>
                            <li>Securely share Custom GPTs within your workspace.</li>
                            <li>Higher message caps than Plus.</li>
                            <li><strong>Best for:</strong> Startups with 2+ users who want collaborative AI features, shared custom tools, and centralized management. Good for teams heavily relying on AI.</li>
                        </ul>
                    </li>
                    <li><strong>ChatGPT Enterprise:</strong>
                        <ul>
                            <li>Custom pricing, contact sales.</li>
                            <li>Unlimited high-speed GPT-4, extended context windows.</li>
                            <li>Advanced security, privacy, and admin controls (SSO, domain verification).</li>
                            <li><strong>Best for:</strong> Larger startups or those with stringent data security and compliance needs, requiring robust AI governance.</li>
                        </ul>
                    </li>
                    <li><strong>API Pricing:</strong> Pay-as-you-go based on token usage for different models if building custom applications.</li>
                </ul>
                <p><strong>Recommendation for Startups:</strong> Start with the Free plan. If core team members find high value and hit limits or need GPT-4/advanced features, upgrade individuals to Plus. Consider Team when you need collaborative features or have several Plus users.</p>
            """,
            "action_steps": create_list_html([
                ("<strong>Day 1: Explore Free Tier & Prompt Basics.</strong> Have key team members sign up for the free ChatGPT. Practice writing clear, contextual prompts for simple tasks (email draft, idea list). Focus: Basic Interaction.", ""),
                ("<strong>Day 2-3 (if considering Plus/Team): Trial Advanced Features.</strong> If viable, have one power user try ChatGPT Plus. Experiment with GPT-4 for a complex task, try one relevant Plugin, and build a simple Custom GPT for an internal FAQ. Focus: Evaluate Premium Value.", ""),
                ("<strong>Day 4: Identify a Bottleneck.</strong> Pick one specific startup bottleneck (e.g., slow blog production, repetitive customer query). Dedicate a session to using ChatGPT (appropriate tier) to address it. Focus: Problem Solving.", ""),
                ("<strong>Day 5: Develop a Use Case Playbook.</strong> Based on the week's experiments, document 2-3 specific, repeatable ways ChatGPT can be used by your team, including example prompts. Focus: Standardize Usage.", "")
            ], list_class="action-steps-list", bold_first=False),
             "pros_cons_startup": create_pros_cons_html(
                pros=[
                    ("Highly Versatile: Applicable across many startup functions.", "Access to Powerful Models (GPT-4 on paid tiers): State-of-the-art capabilities."),
                    ("Extensive Feature Set (Paid Tiers): Plugins, Custom GPTs, Data Analysis, DALL·E offer huge utility.", "Strong Coding & Technical Assistance: Valuable for tech startups."),
                    ("Growing Ecosystem & API: Allows for custom solutions and integrations.")
                ],
                cons=[
                    ("Cost for Advanced Features: GPT-4 and full features require subscription, which can add up for a team.", "Free Tier Limitations: GPT-3.5 is less capable and can be slower or at capacity."),
                    ("Potential for Misinformation: Responses, especially from older models or on complex topics, need verification.", "Learning Curve for Advanced Features: Maximizing plugins or Custom GPTs takes some effort."),
                    ("Data Privacy (OpenAI API has clearer data policies than consumer ChatGPT, Enterprise offers more control): Startups must be mindful of data shared with consumer versions.")
                ]
            ),
            "resources_startup": """
                <ul>
                    <li><a href="https://help.openai.com/en/collections/6769430-chatgpt" target="_blank" rel="noopener noreferrer">OpenAI ChatGPT Help Center:</a> Official guides and FAQs.</li>
                    <li><a href="https://openai.com/blog" target="_blank" rel="noopener noreferrer">OpenAI Blog:</a> For updates on models and features.</li>
                    <li><a href="https://platform.openai.com/docs" target="_blank" rel="noopener noreferrer">OpenAI API Documentation:</a> For developers looking to build custom integrations.</li>
                    <li><strong>Prompt Engineering Guides:</strong> Search for "ChatGPT prompt engineering best practices" for many community and expert resources.</li>
                </ul>
            """
        }
    },
    # --- Claude ---
    "claude": {
        "name": "Anthropic Claude",
        "startup_tagline": "The safety-focused AI for reliable text generation, summarization, and complex reasoning, with industry-leading context windows.",
        "logo_url": "/static/img/claude-logo.png",
        "official_link": "https://claude.ai/",
        "cta_link": "https://claude.ai/login",
        "cta_text": "Try Claude",
        "sections": {
            "intro_startup": "Why Claude for Your Startup?",
            "features_startup": "Key Claude Features for Startup Success",
            "getting_started_startup": "Getting Started with Claude (Free & Pro)",
            "use_cases_startup": "Claude in Action: Startup Use Cases",
            "integration_startup": "Claude API & Integrations for Startups",
            "roi_startup": "Claude's ROI: Reliability and Long-Context Value",
            "pricing_startup": "Claude Pricing for Startups",
            "action_steps": "Your First Week with Claude: Quick Wins",
            "pros_cons_startup": "Claude: Pros & Cons for Startups",
            "resources_startup": "Further Learning & Support"
        },
        "content": {
            "intro_startup": """
                <p>Anthropic's Claude family of models (Claude 3 Opus, Sonnet, Haiku) offers startups a powerful AI assistant with a strong emphasis on safety, reliability, and handling extensive information. If your startup deals with large documents, needs nuanced understanding, or prioritizes responsible AI, Claude is a compelling choice.</p>
                <p>Startups can leverage Claude to:</p>
                <ul>
                    <li><strong>Process & Analyze Large Datasets:</strong> Claude's large context window (up to 200K tokens, equivalent to ~150,000 words) is ideal for summarizing long reports, legal documents, codebases, or entire books.</li>
                    <li><strong>Enhance Customer Support:</strong> Draft accurate and empathetic customer responses, or power sophisticated FAQ bots.</li>
                    <li><strong>Conduct In-depth Research:</strong> Analyze multiple sources simultaneously to extract insights and synthesize information.</li>
                    <li><strong>Improve Content Quality:</strong> Generate well-reasoned, coherent, and less prone-to-harmful-output content.</li>
                    <li><strong>Develop with Confidence (API):</strong> Build AI applications knowing Claude is designed with safety principles like Constitutional AI at its core.</li>
                </ul>
            """,
            "features_startup": create_list_html([
                ("Industry-Leading Context Window (Claude 3)", "Process and reason over vast amounts of text (up to 200K tokens with Opus), perfect for long-form content analysis, RAG systems, and complex Q&A."),
                ("Strong Reasoning & Comprehension", "Excels at understanding nuance, complex instructions, and performing multi-step reasoning tasks."),
                ("High Accuracy & Reduced Hallucinations", "Engineered for greater factuality and less confabulation compared to some other models."),
                ("Safety-Focused Design (Constitutional AI)", "Built with principles to make it helpful, harmless, and honest, crucial for brand reputation."),
                ("Multiple Model Tiers (Opus, Sonnet, Haiku)", "Choose the right balance of intelligence, speed, and cost for your specific startup needs (Haiku for speed/cost, Sonnet for balance, Opus for max power)."),
                ("Image Understanding (Claude 3)", "Analyze and interpret visual information from images, charts, and diagrams."),
                ("Strong Coding Capabilities", "Assists with code generation, debugging, and explanation across various programming languages."),
                ("API Access", "Robust API for developers to integrate Claude into custom applications and workflows.")
            ], list_class="key-feature-list", bold_first=True),
            "getting_started_startup": """
                <p>Getting your startup started with Claude:</p>
                <ol>
                    <li><strong>Access Claude:</strong>
                        <ul>
                            <li><strong>claude.ai:</strong> Web interface for direct interaction. Sign up for free access (usually to Sonnet, with limits).</li>
                            <li><strong>Claude Pro:</strong> Subscription for higher usage limits, priority access, and access to all models including Opus.</li>
                            <li><strong>API Access:</strong> Request API keys via the Anthropic Console if you plan to build custom integrations.</li>
                        </ul>
                    </li>
                    <li><strong>Understand Model Tiers (Claude 3):</strong>
                        <ul>
                            <li><strong>Haiku:</strong> Fastest and most affordable, good for quick summarization, simple Q&A, and chatbots.</li>
                            <li><strong>Sonnet:</strong> Balanced performance and cost, excellent for most enterprise workloads, content generation, and data extraction. (Often the default in free claude.ai)</li>
                            <li><strong>Opus:</strong> Most powerful model, for highly complex tasks, deep reasoning, R&D, and strategic analysis.</li>
                        </ul>
                    </li>
                    <li><strong>Prompting Best Practices:</strong>
                        <ul>
                            <li>Be explicit with instructions. Claude responds well to clear, detailed prompts.</li>
                            <li>Utilize its large context window by providing ample background information directly in the prompt.</li>
                            <li>For complex tasks, break them down into steps.</li>
                        </ul>
                    </li>
                    <li><strong>Explore Use Cases:</strong> Start by using claude.ai for tasks like summarizing a long article, drafting a detailed email, or asking complex questions based on provided text.</li>
                </ol>
            """,
             "use_cases_startup": """
                <h4>Legal & Compliance:</h4>
                <ul>
                    <li><strong>Document Review:</strong> "Summarize the key obligations for our startup in this 50-page SaaS agreement: [paste text]." (Always verify with legal counsel)</li>
                    <li><strong>Policy Drafting:</strong> "Help me draft an initial version of a privacy policy for a mobile app that collects user analytics."</li>
                </ul>
                <h4>Research & Development:</h4>
                <ul>
                    <li><strong>Literature Review:</strong> "Analyze these 5 research papers on [topic] and identify common themes and future research directions: [paste abstracts or full text if within context limit]."</li>
                    <li><strong>Technical Problem Solving:</strong> "I'm encountering [specific error] with [technology]. Here's my setup: [details]. What are potential causes and solutions?"</li>
                </ul>
                <h4>Customer Support & Operations:</h4>
                <ul>
                    <li><strong>Complex Query Handling:</strong> "A customer has this complex issue: [describe issue]. Draft a comprehensive and empathetic response outlining troubleshooting steps."</li>
                    <li><strong>Knowledge Base Creation:</strong> "Convert these product update notes into a user-friendly FAQ section for our knowledge base: [paste notes]."</li>
                </ul>
                <h4>Content & Strategy:</h4>
                <ul>
                    <li><strong>In-depth Article Generation:</strong> "Write a 1500-word article on the impact of AI on the future of remote work, citing potential benefits and challenges."</li>
                    <li><strong>Financial Analysis (with provided data):</strong> "Given this financial data [paste data or describe], what are some key trends and areas for improvement?" (Requires careful data input)</li>
                </ul>
            """,
            "integration_startup": """
                <p>Anthropic provides robust API access for startups to integrate Claude's intelligence:</p>
                <ul>
                    <li><strong>Claude API:</strong>
                        <ul>
                            <li>The primary way to build custom applications. Available via the Anthropic Console.</li>
                            <li>Supports all Claude 3 models (Opus, Sonnet, Haiku) allowing you to choose the best fit for cost and performance.</li>
                            <li>Well-documented with client libraries for popular languages (Python, Node.js).</li>
                            <li><em>Startup Use Cases:</em> Custom internal tools for document analysis, AI-powered features in your SaaS product, intelligent chatbots, automated reporting.</li>
                        </ul>
                    </li>
                    <li><strong>Third-Party Platforms & Tools:</strong>
                        <ul>
                            <li>Claude is increasingly available on major cloud provider platforms (e.g., AWS Bedrock, Google Vertex AI Model Garden). This can simplify deployment and MLOps for startups already using these clouds.</li>
                            <li>Integration with automation platforms like Zapier or Make.com might be possible via their API connectors, allowing no-code/low-code workflows.</li>
                        </ul>
                    </li>
                    <li><strong>Partner Ecosystem:</strong> Anthropic is building a partner ecosystem, so look out for tools and services that offer native Claude integrations.</li>
                </ul>
                <p><strong>For Startups:</strong> If you need to analyze large volumes of text or require highly reliable AI responses within your own products or workflows, investing in API integration can provide significant competitive advantages.</p>
            """,
            "roi_startup": """
                <p>Claude's ROI for startups, particularly when using Pro or the API, stems from its unique strengths:</p>
                <ul>
                    <li><strong>Efficiency with Large Documents:</strong> Time saved on reading, summarizing, and extracting information from long reports, contracts, or research papers can be immense. This directly translates to faster decision-making and reduced manual labor.</li>
                    <li><strong>Higher Quality Outputs & Reduced Rework:</strong> Claude's focus on accuracy and coherence can mean less time spent editing and correcting AI-generated content, improving overall productivity.</li>
                    <li><strong>Handling Complex Tasks:</strong> Its strong reasoning capabilities allow it to tackle tasks that simpler models might struggle with, potentially unlocking new automation opportunities or insights.</li>
                    <li><strong>Risk Mitigation (Safety Focus):</strong> For startups concerned about brand reputation and responsible AI use, Claude's safety features can reduce the risk of generating inappropriate or harmful content, saving potential C-suite headaches.</li>
                    <li><strong>Competitive Differentiation (API):</strong> Building unique AI features into your product using Claude's advanced capabilities (like its large context window for hyper-personalization or deep document Q&A) can create strong market differentiation.</li>
                </ul>
                <p><strong>Measuring ROI:</strong> Track time spent on document-heavy tasks before and after Claude. Monitor content quality and error rates. If using the API, measure the impact of new AI features on user engagement, retention, or sales.</p>
            """,
            "pricing_startup": """
                <p>Anthropic's pricing for Claude is tiered:</p>
                <ul>
                    <li><strong>claude.ai (Web Interface - Free Tier):</strong>
                        <ul>
                            <li>Typically provides access to a capable model like Claude 3 Sonnet.</li>
                            <li>Subject to usage limits (e.g., daily message caps).</li>
                            <li><strong>Best for:</strong> Individual experimentation, occasional use, startups testing the waters.</li>
                        </ul>
                    </li>
                    <li><strong>Claude Pro (Web Interface - Subscription):</strong>
                        <ul>
                            <li>Around $20/month per user.</li>
                            <li>Significantly higher usage limits than the free tier.</li>
                            <li>Priority access during peak times.</li>
                            <li>Access to all Claude 3 models (Opus, Sonnet, Haiku) via the web UI.</li>
                            <li><strong>Best for:</strong> Founders and team members who frequently use Claude for demanding tasks and need its full power via the chat interface.</li>
                        </ul>
                    </li>
                    <li><strong>Claude API (Pay-as-you-go):</strong>
                        <ul>
                            <li>Pricing is based on the number of input and output tokens (like words/parts of words).</li>
                            <li>Different rates for each model:
                                <ul>
                                    <li><strong>Claude 3 Haiku:</strong> Most affordable, designed for speed.</li>
                                    <li><strong>Claude 3 Sonnet:</strong> Balanced cost and performance.</li>
                                    <li><strong>Claude 3 Opus:</strong> Most powerful, highest price per token.</li>
                                </ul>
                            </li>
                            <li>Pricing details are available on the Anthropic website.</li>
                            <li><strong>Best for:</strong> Startups building custom applications, automating workflows, or needing programmatic access to Claude's capabilities. Allows fine-grained cost control based on actual usage.</li>
                        </ul>
                    </li>
                </ul>
                <p><strong>Startup Strategy:</strong> Use the free tier of claude.ai for initial evaluation. Upgrade key users to Pro if web UI power is needed. For embedding AI or high-volume processing, budget for API usage, starting with Sonnet or Haiku for cost-effectiveness and scaling to Opus for tasks requiring maximum intelligence.</p>
            """,
            "action_steps": create_list_html([
                ("<strong>Day 1: Long Document Summarization.</strong> Find a lengthy internal document or public report relevant to your startup. Use claude.ai (free tier) to summarize its key points. Test its ability to condense information accurately. Focus: Context Handling.", ""),
                ("<strong>Day 2-3: Complex Q&A.</strong> Provide Claude with a detailed document (e.g., product specs, a dense article) and ask specific, nuanced questions that require understanding relationships within the text. Focus: Comprehension & Reasoning.", ""),
                ("<strong>Day 4 (if considering Pro/API): Test Model Tiers.</strong> If Pro access is available, compare responses from Sonnet and Opus for the same complex prompt. If exploring API, send a test request to Haiku and Sonnet to compare speed and quality for a specific task. Focus: Model Evaluation.", ""),
                ("<strong>Day 5: Identify a High-Value, Text-Intensive Workflow.</strong> Pinpoint a task in your startup that involves significant manual text processing (e.g., customer support ticket analysis, contract review pre-legal, market research synthesis). Brainstorm how Claude could streamline it. Focus: Application Ideation.", "")
            ], list_class="action-steps-list", bold_first=False),
            "pros_cons_startup": create_pros_cons_html(
                pros=[
                    ("Excellent Long-Context Handling: Ideal for deep document analysis and complex Q&A.", "Strong Reasoning & Reliability: Produces coherent and often more accurate outputs."),
                    ("Safety-Focused Design: Lower risk of generating problematic content, good for brand-sensitive startups.", "Tiered Models (Opus, Sonnet, Haiku): Flexibility to balance power, speed, and cost."),
                    ("Competitive API: Good for building robust, custom AI solutions.")
                ],
                cons=[
                    ("Web UI (claude.ai) Features: While improving, it might have fewer bells and whistles (like plugins) than some competitors' web UIs, focusing more on core chat.", "Cost of Opus Model (API & Pro): The most powerful model comes at a premium, requiring clear ROI justification for startups."),
                    ("Smaller Ecosystem (Historically): Anthropic's ecosystem of third-party tools and integrations is growing but might have been smaller than OpenAI's initially.", "Name Recognition: While highly respected, 'Claude' might be less known to general staff than 'ChatGPT'.")
                ]
            ),
            "resources_startup": """
                <ul>
                    <li><a href="https://www.anthropic.com/product" target="_blank" rel="noopener noreferrer">Anthropic Product Page:</a> Overview of Claude models.</li>
                    <li><a href="https://docs.anthropic.com/claude/reference/getting-started-with-the-api" target="_blank" rel="noopener noreferrer">Anthropic API Documentation:</a> Essential for developers.</li>
                    <li><a href="https://www.anthropic.com/news" target="_blank" rel="noopener noreferrer">Anthropic News/Blog:</a> For research, updates, and use cases.</li>
                    <li><a href="https://console.anthropic.com/docs/prompt-engineering" target="_blank" rel="noopener noreferrer">Anthropic Prompt Engineering Guide:</a> Official tips for getting the best out of Claude.</li>
                </ul>
            """
        }
    },
    # --- Gemini ---
    "gemini": {
        "name": "Google Gemini",
        "startup_tagline": "Google's natively multimodal AI, powering next-gen applications with versatile intelligence tiers (Ultra, Pro, Nano).",
        "logo_url": "/static/img/gemini-logo.png",
        "official_link": "https://deepmind.google/technologies/gemini/",
        "cta_link": "https://ai.google.dev/", # Google AI Studio for developers
        "cta_text": "Explore Gemini for Developers",
        "sections": {
            "intro_startup": "Why Gemini for Your Startup?",
            "features_startup": "Key Gemini Features for Startup Innovation",
            "getting_started_startup": "Accessing Gemini: Bard, AI Studio & APIs",
            "use_cases_startup": "Gemini in Action: Multimodal Startup Use Cases",
            "integration_startup": "Building with Gemini: APIs and Google Cloud",
            "roi_startup": "Gemini's ROI: Multimodal Advantage for Startups",
            "pricing_startup": "Gemini Pricing via Google Cloud & Products",
            "action_steps": "Your First Week with Gemini: Quick Wins",
            "pros_cons_startup": "Gemini: Pros & Cons for Startups",
            "resources_startup": "Further Learning & Developer Tools"
        },
        "content": {
            "intro_startup": """
                <p>Google Gemini represents Google's most advanced and flexible suite of AI models, designed from the ground up to be natively multimodal. This means Gemini can seamlessly understand, operate across, and combine different types of information like text, code, images, audio, and video. For startups, Gemini opens doors to building truly innovative applications and gaining deeper insights from diverse data sources.</p>
                <p>Gemini comes in different sizes for various needs:</p>
                <ul>
                    <li><strong>Gemini Ultra:</strong> The largest and most capable model for highly complex tasks.</li>
                    <li><strong>Gemini Pro:</strong> A versatile model for scaling across a wide range of tasks, often powering tools like Bard.</li>
                    <li><strong>Gemini Nano:</strong> The most efficient model for on-device tasks (e.g., on Pixel phones).</li>
                </ul>
                <p>Startups can use Gemini to:</p>
                <ul>
                    <li><strong>Develop Next-Gen Multimodal Apps:</strong> Create experiences that blend text, image, and potentially other modalities.</li>
                    <li><strong>Enhance Data Analysis:</strong> Extract insights from text combined with images, charts, or even video content.</li>
                    <li><strong>Power Sophisticated AI Agents:</strong> Build systems that can perceive, reason, and act based on diverse inputs.</li>
                    <li><strong>Future-Proof AI Strategy:</strong> Align with Google's cutting-edge AI research and development.</li>
                </ul>
            """,
            "features_startup": create_list_html([
                ("Native Multimodality", "Seamlessly understands and reasons across text, code, images, and (increasingly) audio/video without needing separate models for each."),
                ("State-of-the-Art Performance", "Achieves top-tier results on a wide range of industry benchmarks for text, coding, reasoning, and multimodal tasks."),
                ("Scalable Model Sizes (Ultra, Pro, Nano)", "Choose the optimal model for your startup's specific performance, cost, and deployment needs (e.g., cloud vs. on-device)."),
                ("Advanced Reasoning & Coding", "Sophisticated capabilities in logical deduction, problem-solving, and generating high-quality code in various languages."),
                ("Integration with Google Ecosystem", "Powers flagship Google products (like Bard) and is deeply integrated into Google Cloud (Vertex AI) and developer tools (Google AI Studio)."),
                ("Fine-Tuning Capabilities (Vertex AI)", "Startups can fine-tune Gemini models on their own data for specialized tasks and improved performance in their specific domain."),
                ("Responsible AI Toolkit", "Access to Google's tools and best practices for building AI applications responsibly.")
            ], list_class="key-feature-list", bold_first=True),
            "getting_started_startup": """
                <p>Startups can access Gemini's capabilities through several channels:</p>
                <ol>
                    <li><strong>Google Bard:</strong> The easiest way to experience Gemini Pro's text and image capabilities. Use Bard for brainstorming, content creation, and multimodal queries (e.g., "What's interesting about this image? [upload image]").</li>
                    <li><strong>Google AI Studio:</strong>
                        <ul>
                            <li>A free, web-based tool for developers to quickly prototype and run prompts with Gemini Pro (and other Google models).</li>
                            <li>Generate API keys to easily transfer your work into applications.</li>
                            <li>Visit <a href="https://ai.google.dev/" target="_blank">ai.google.dev</a> to get started.</li>
                        </ul>
                    </li>
                    <li><strong>Vertex AI (Google Cloud):</strong>
                        <ul>
                            <li>Google Cloud's unified machine learning platform. Offers access to Gemini Pro and potentially Gemini Ultra for enterprise-grade applications.</li>
                            <li>Provides tools for MLOps, fine-tuning, deployment, and scaling AI models.</li>
                            <li>Requires a Google Cloud Platform account.</li>
                        </ul>
                    </li>
                    <li><strong>On-Device (Gemini Nano):</strong> For mobile-first startups, Gemini Nano powers features on select Android devices (e.g., Pixel 8 Pro). Direct developer access for custom on-device apps may evolve.</li>
                </ol>
                <p><strong>Recommendation for Startups:</strong> Start with Bard for general use. Developers should explore Google AI Studio for rapid prototyping. For production applications or fine-tuning, Vertex AI is the path.</p>
            """,
            "use_cases_startup": """
                <h4>Multimodal Applications:</h4>
                <ul>
                    <li><strong>Visual Q&A:</strong> "Analyze this uploaded product image and generate a compelling marketing description highlighting its key visual features."</li>
                    <li><strong>Content Creation from Visuals:</strong> "Create a social media post script based on the story told in this short video clip [if video input supported/described]."</li>
                    <li><strong>Data Entry from Images:</strong> "Extract all text and structured data (like table contents) from this scanned invoice image."</li>
                </ul>
                <h4>Advanced Text & Code Tasks:</h4>
                <ul>
                    <li><strong>Complex System Design:</strong> "Help me outline the architecture for a scalable e-commerce backend using microservices, and suggest key technologies."</li>
                    <li><strong>Cross-Language Code Translation & Explanation:</strong> "Translate this Python script to JavaScript and explain the key differences in how they handle asynchronous operations."</li>
                </ul>
                <h4>Data Analysis & Insights:</h4>
                <ul>
                    <li><strong>Trend Identification from Mixed Data:</strong> "Analyze this report containing text, charts, and tables [describe or provide access if API allows] to identify the top 3 emerging market opportunities."</li>
                    <li><strong>Automated Report Generation:</strong> "Generate a weekly sales summary based on input data, including natural language explanations of key performance indicators."</li>
                </ul>
            """,
            "integration_startup": """
                <p>Integrating Gemini into your startup's products and workflows is primarily done through Google's developer platforms:</p>
                <ul>
                    <li><strong>Gemini API (via Google AI Studio & Vertex AI):</strong>
                        <ul>
                            <li>Provides programmatic access to Gemini Pro (and potentially Ultra in Vertex AI).</li>
                            <li>REST APIs and client libraries (Python, Node.js, Java, Go, etc.) make it easy to incorporate Gemini into your applications.</li>
                            <li>Use cases: Powering custom chatbots, generating dynamic content, analyzing user-uploaded multimodal data, creating AI-driven features in your SaaS product.</li>
                        </ul>
                    </li>
                    <li><strong>Vertex AI Platform:</strong>
                        <ul>
                            <li>Offers a comprehensive environment for building, deploying, and managing Gemini-powered applications at scale.</li>
                            <li><strong>Fine-tuning:</strong> Adapt Gemini Pro to your specific domain or dataset for enhanced performance on niche tasks. This is a powerful feature for startups wanting highly specialized AI.</li>
                            <li><strong>Vector Search:</strong> Build sophisticated RAG (Retrieval Augmented Generation) systems by combining Gemini with vector databases to ground responses in your company's knowledge.</li>
                            <li><strong>MLOps Tools:</strong> Manage the entire lifecycle of your AI models.</li>
                        </ul>
                    </li>
                    <li><strong>Firebase Extensions (Potential):</strong> Google may offer Firebase Extensions that make it easier to integrate Gemini capabilities into mobile and web apps built with Firebase.</li>
                    <li><strong>Integration with other Google Cloud Services:</strong> Combine Gemini with services like Google Cloud Storage, BigQuery, Pub/Sub, etc., to build robust data pipelines and AI workflows.</li>
                </ul>
                <p><strong>Startup Tip:</strong> Google AI Studio is excellent for quick API key generation and initial app development. For production, robust deployment, and fine-tuning, transitioning to Vertex AI is recommended.</p>
            """,
            "roi_startup": """
                <p>Gemini's ROI for startups lies in its ability to unlock new types of value through multimodality and advanced intelligence:</p>
                <ul>
                    <li><strong>Innovative Product Features:</strong> Developing unique multimodal experiences (e.g., an app that understands user-drawn sketches and text prompts) can create significant competitive moats and attract customers.</li>
                    <li><strong>Deeper Insights from Diverse Data:</strong> Startups often have data in various formats (text, images from user uploads, etc.). Gemini can help analyze this holistic data for richer insights than text-only models.</li>
                    <li><strong>Enhanced Automation:</strong> Automate tasks that require understanding both visual and textual information, such as processing visually rich documents or moderating user-generated multimodal content.</li>
                    <li><strong>Efficiency in Specialized Tasks:</strong> Gemini's strong performance in coding, complex reasoning, and science/math can accelerate R&D and specialized problem-solving for tech-heavy startups.</li>
                    <li><strong>Cost-Effectiveness (Tiered Models):</strong> The ability to choose between Ultra, Pro, and Nano (and fine-tune Pro) allows startups to optimize cost vs. performance for different applications.</li>
                </ul>
                <p><strong>Considerations for ROI:</strong> Building true multimodal applications requires design and development effort. The ROI often comes from creating superior user experiences or highly efficient new workflows that weren't possible before.</p>
            """,
            "pricing_startup": """
                <p>Pricing for Gemini capabilities is typically accessed through Google Cloud (Vertex AI) or Google AI Studio, and may be part of products like Bard.</p>
                <ul>
                    <li><strong>Google AI Studio (Gemini Pro):</strong>
                        <ul>
                            <li>Often has a free tier for experimentation with rate limits.</li>
                            <li>Pay-as-you-go pricing for API calls beyond the free tier, based on input/output characters or tokens.</li>
                        </ul>
                    </li>
                    <li><strong>Vertex AI (Gemini Pro, potentially Ultra):</strong>
                        <ul>
                            <li>Pricing is per 1,000 characters or tokens (input and output), and can vary if images or other modalities are involved.</li>
                            <li>Fine-tuning Gemini models on Vertex AI will have associated training and hosting costs.</li>
                            <li>Google Cloud offers a free tier and credits for new startups, which can help offset initial costs. Check current Google Cloud Free Program details.</li>
                        </ul>
                    </li>
                    <li><strong>Bard (powered by Gemini Pro):</strong> The consumer-facing Bard is generally free, providing an accessible way to experience Gemini's power.</li>
                    <li><strong>Gemini Nano (On-device):</strong> No direct cost to the startup for the model itself if it's part of the OS/device features; costs are associated with app development.</li>
                </ul>
                <p><strong>Key for Startups:</strong>
                    Always check the official <a href="https://cloud.google.com/vertex-ai/pricing" target="_blank">Vertex AI pricing page</a> and <a href="https://ai.google.dev/pricing" target="_blank">Google AI Studio pricing</a> for the latest details.
                    Factor in potential Google Cloud credits.
                    Start with the most cost-effective model (e.g., Gemini Pro via AI Studio) and scale as needed.
                </p>
            """,
            "action_steps": create_list_html([
                ("<strong>Day 1: Experience Multimodality in Bard.</strong> If you have an image (e.g., a chart, a product photo), upload it to Bard (which uses Gemini Pro) and ask questions about it or ask for a description. Focus: Understanding Visual Input.", ""),
                ("<strong>Day 2-3 (Developers): Prototype with Google AI Studio.</strong> Sign up for Google AI Studio. Try a few text prompts with Gemini Pro. Then, attempt a multimodal prompt if supported in the UI (e.g., providing an image URL with a text query). Get an API key. Focus: Developer Familiarization.", ""),
                ("<strong>Day 4: Identify a Multimodal Opportunity.</strong> Think about your startup's data or user interactions. Is there a place where combining text and image (or other modalities) could create significant value or solve a pain point? (e.g., analyzing user-submitted photos, understanding diagrams in support tickets). Focus: Use Case Ideation.", ""),
                ("<strong>Day 5: Explore a Simple API Call.</strong> Using the API key from AI Studio, have a developer make a basic Gemini Pro API call from a simple script (e.g., Python) to send a text prompt and receive a response. Focus: Basic API Integration.", "")
            ], list_class="action-steps-list", bold_first=False),
            "pros_cons_startup": create_pros_cons_html(
                pros=[
                    ("Truly Natively Multimodal: Unlocks new application types and deeper data understanding.", "State-of-the-Art Performance: Excellent across a wide range of difficult tasks."),
                    ("Scalable Models (Ultra, Pro, Nano): Options for different needs and budgets.", "Strong Google Ecosystem Integration: Leverages Google Cloud, AI Studio, and powers tools like Bard."),
                    ("Fine-Tuning on Vertex AI: Allows deep customization for specific startup domains.")
                ],
                cons=[
                    ("Complexity for Full Potential: Leveraging true multimodality or fine-tuning often requires more development effort than text-only models.", "Cost of Advanced Tiers/Vertex AI: Gemini Ultra or extensive Vertex AI usage can be costly; startups need clear ROI.", "Newer API/Ecosystem: While robust, the developer ecosystem around Gemini might still be maturing in some niche areas compared to longer-established text-only APIs."),
                    ("Access to Gemini Ultra: Might be more limited or enterprise-focused initially through Vertex AI compared to Pro.")
                ]
            ),
            "resources_startup": """
                <ul>
                    <li><a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">Google AI for Developers:</a> Hub for Gemini API, Google AI Studio, and documentation.</li>
                    <li><a href="https://deepmind.google/technologies/gemini/#hands-on" target="_blank" rel="noopener noreferrer">Gemini Official Page (DeepMind):</a> Technical reports and overview.</li>
                    <li><a href="https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview" target="_blank" rel="noopener noreferrer">Vertex AI Generative AI Overview:</a> Documentation for using Gemini on Google Cloud.</li>
                    <li><a href="https://www.youtube.com/GoogleDevelopers" target="_blank" rel="noopener noreferrer">Google Developers YouTube Channel:</a> Often features tutorials and updates on Gemini.</li>
                </ul>
            """
        }
    },
    # --- Notion AI ---
    "notionai": {
        "name": "Notion AI",
        "startup_tagline": "Supercharge your startup's productivity by embedding AI directly into your Notion workspace for writing, summarizing, and task management.",
        "logo_url": "/static/img/notion-logo.png",
        "official_link": "https://www.notion.so/product/ai",
        "cta_link": "https://www.notion.so/product/ai",
        "cta_text": "Add Notion AI to Your Workspace",
        "sections": {
            "intro_startup": "Why Notion AI for Your Startup's OS?",
            "features_startup": "Key Notion AI Features for Peak Productivity",
            "getting_started_startup": "Activating & Using Notion AI in Your Workspace",
            "use_cases_startup": "Notion AI in Action: Streamlining Startup Operations",
            "integration_startup": "Leveraging Notion AI within Your Notion Ecosystem",
            "roi_startup": "Notion AI's ROI: Enhanced Team Collaboration & Efficiency",
            "pricing_startup": "Notion AI Pricing: An Add-on for Your Workspace",
            "action_steps": "Your First Week with Notion AI: Quick Wins",
            "pros_cons_startup": "Notion AI: Pros & Cons for Startups",
            "resources_startup": "Further Learning & Notion Community"
        },
        "content": {
            "intro_startup": """
                <p>If your startup runs on Notion for documentation, project management, and knowledge sharing, Notion AI is a natural extension to boost your team's productivity. It brings AI capabilities directly into your existing workflows, helping you write faster, summarize information, brainstorm ideas, and manage tasks more effectively—all without leaving Notion.</p>
                <p>Notion AI acts as a contextual assistant within your workspace, understanding the content on your pages to provide relevant help. Startups can use it to:</p>
                <ul>
                    <li><strong>Standardize & Accelerate Documentation:</strong> Quickly draft SOPs, meeting notes, project plans, and knowledge base articles.</li>
                    <li><strong>Improve Written Communication:</strong> Enhance clarity, tone, and grammar for internal and external comms.</li>
                    <li><strong>Automate Summaries & Action Items:</strong> Instantly get key takeaways from long pages or meeting notes.</li>
                    <li><strong>Boost Team Collaboration:</strong> Use AI to brainstorm, outline projects, and generate first drafts collaboratively.</li>
                </ul>
            """,
            "features_startup": create_list_html([
                ("Integrated Writing Assistant", "Improve writing, fix spelling/grammar, change tone, translate, shorten, or lengthen text directly within any Notion page."),
                ("Summarization & Action Item Extraction", "Quickly get summaries of long documents or extract actionable tasks from meeting notes."),
                ("Content Generation", "Draft blog posts, emails, job descriptions, social media updates, or outlines from a simple prompt."),
                ("Brainstorming & Ideation", "Generate lists of ideas, pros & cons, or different perspectives on a topic."),
                ("AI Blocks", "Dedicated blocks for specific AI tasks like Summary, Action Items, or Custom AI Prompts within your Notion structure."),
                ("Q&A on Your Workspace (Contextual)", "Ask questions about your Notion content, and AI can search and synthesize answers from your knowledge base (feature may evolve)."),
                ("Autofill from Page Content", "Use AI to intelligently populate database properties based on the content of a page.")
            ], list_class="key-feature-list", bold_first=True),
            "getting_started_startup": """
                <p>Integrating Notion AI into your startup's Notion workspace:</p>
                <ol>
                    <li><strong>Notion AI Subscription:</strong> Notion AI is an add-on to your existing Notion plan (Free, Plus, Business, or Enterprise). You'll need to add it to your workspace via your Notion settings (usually under "Settings & Members" > "Plans" or "Upgrade").</li>
                    <li><strong>Accessing Notion AI:</strong>
                        <ul>
                            <li><strong>Spacebar Prompt:</strong> On a new line or selected text in a Notion page, press the `Spacebar` to bring up the AI prompt menu.</li>
                            <li><strong>Slash Command:</strong> Type `/ai` to see AI options.</li>
                            <li><strong>AI Blocks:</strong> Insert specific AI blocks like `/summary` or `/action items`.</li>
                        </ul>
                    </li>
                    <li><strong>Key Actions to Try:</strong>
                        <ul>
                            <li><strong>Improve Writing:</strong> Select some text you've written and ask AI to "Improve writing," "Make shorter," or "Change tone to professional."</li>
                            <li><strong>Summarize:</strong> On a page with lots of text, use the "Summarize" option.</li>
                            <li><strong>Draft Content:</strong> On a new line, type "Write a blog post about [topic]" and let AI generate a first draft.</li>
                        </ul>
                    </li>
                    <li><strong>Team Onboarding:</strong> Encourage all Notion users in your startup to explore these features. Share successful prompts and use cases in a central Notion page.</li>
                </ol>
            """,
             "use_cases_startup": """
                <h4>Project Management & Documentation:</h4>
                <ul>
                    <li><strong>Meeting Note Automation:</strong> After a meeting, paste raw notes into Notion and use AI to "Summarize" and "Find action items."</li>
                    <li><strong>Project Planning:</strong> "Create a project plan outline for launching a new website, including key phases and tasks."</li>
                    <li><strong>SOP Drafting:</strong> "Draft an SOP for onboarding new marketing hires."</li>
                </ul>
                <h4>Content & Marketing:</h4>
                <ul>
                    <li><strong>Blog Post Outlines & Drafts:</strong> "Generate 5 blog post ideas about [your industry trend]. Then, write an outline for the first idea."</li>
                    <li><strong>Social Media Content:</strong> "Write 3 tweets announcing our new product feature: [feature description]."</li>
                    <li><strong>Website Copy Improvement:</strong> Select text on your Notion-drafted landing page and ask AI to "Make more persuasive."</li>
                </ul>
                <h4>HR & Operations:</h4>
                <ul>
                    <li><strong>Job Descriptions:</strong> "Draft a job description for a [Role] at a fast-growing tech startup."</li>
                    <li><strong>Internal Announcements:</strong> "Write a friendly internal announcement about our upcoming company offsite."</li>
                </ul>
                <h4>Personal Productivity:</h4>
                <ul>
                    <li><strong>Brainstorming Solutions:</strong> "List pros and cons of switching to a new CRM system for our sales team."</li>
                    <li><strong>Learning & Explanation:</strong> "Explain [complex concept] in simple terms."</li>
                </ul>
            """,
            "integration_startup": """
                <p>Notion AI's primary integration is, by design, deeply embedded <strong>within the Notion ecosystem itself</strong>. It leverages the content and structure of your Notion workspace to provide contextual assistance.</p>
                <ul>
                    <li><strong>Contextual Awareness:</strong> Notion AI can understand the content of the page you're working on, or selected text, to provide more relevant suggestions, summaries, or generations.</li>
                    <li><strong>Database Integration (Autofill):</strong> A powerful feature is using AI to autofill properties in your Notion databases based on the content of a page. For example, automatically summarize a meeting note page into a "Key Takeaways" database property, or extract a due date.</li>
                    <li><strong>AI Blocks for Structure:</strong> Use AI Summary blocks or Action Item blocks to consistently apply AI processing to parts of your documents or templates.</li>
                    <li><strong>Templates with AI:</strong> Build Notion templates for recurring tasks (e.g., meeting notes, project briefs) that include pre-set AI prompts or AI blocks to streamline an AI-assisted workflow.</li>
                </ul>
                <p><strong>External Integrations:</strong> While Notion AI itself doesn't directly integrate with external apps in the same way a tool like Zapier does, your Notion workspace *can* be integrated with other tools (e.g., Slack, Google Calendar, Zapier). The content generated or managed by Notion AI within Notion can then become part of these broader, non-AI automations.</p>
                <p><strong>Startup Tip:</strong> Focus on building robust Notion templates that incorporate AI prompts for common tasks. This standardizes AI use and maximizes efficiency for your team.</p>
            """,
            "roi_startup": """
                <p>For startups already invested in Notion as their central operating system, Notion AI's ROI is primarily about enhancing team productivity and content quality within that familiar environment:</p>
                <ul>
                    <li><strong>Massive Time Savings on Routine Tasks:</strong> Drafting emails, summarizing notes, creating first drafts of documents—these small time savings per task add up significantly across a team.</li>
                    <li><strong>Improved Content Velocity & Quality:</strong> Generate more content (blog posts, SOPs, marketing copy) faster, and use AI to refine it for clarity and tone, leading to better internal and external communication.</li>
                    <li><strong>Enhanced Collaboration:</strong> AI can facilitate brainstorming and help teams quickly get on the same page by summarizing discussions or outlining next steps.</li>
                    <li><strong>Streamlined Knowledge Management:</strong> Use AI to quickly find information within your Notion workspace (via Q&A features) or to make existing knowledge more accessible through summaries.</li>
                    <li><strong>Reduced Friction & Context Switching:</strong> Having AI tools directly within the workspace where work happens minimizes the need to switch to other apps, keeping your team focused.</li>
                </ul>
                <p><strong>Measuring ROI:</strong>
                    Compare the time taken for common Notion-based tasks (e.g., writing meeting summaries, drafting project proposals) before and after implementing Notion AI.
                    Track content output (e.g., number of help articles created, blog posts published).
                    Survey your team on perceived productivity improvements and ease of use.
                </p>
            """,
            "pricing_startup": """
                <p>Notion AI is an <strong>add-on subscription</strong> to your existing Notion plan.</p>
                <ul>
                    <li><strong>Cost:</strong> Typically priced per member, per month (e.g., around $8-$10 per member/month when billed annually, or slightly higher monthly). This cost is *in addition* to your base Notion plan (Free, Plus, Business, Enterprise).</li>
                    <li><strong>Billing:</strong> Added to your workspace bill. All members in the workspace typically get access if AI is added, though this can depend on Notion's specific offering at the time.</li>
                    <li><strong>Trial:</strong> Notion often provides a limited number of free AI actions per workspace or member to try before committing to a subscription.</li>
                </ul>
                <p><strong>Is it worth it for a startup?</strong></p>
                <ul>
                    <li><strong>If your startup heavily uses Notion:</strong> Yes, the productivity gains can easily justify the cost if your team actively uses the AI features. The time saved per employee can quickly exceed the add-on fee.</li>
                    <li><strong>Consider per-user value:</strong> If only a few team members would heavily use AI, assess if their individual productivity gains warrant the cost for those seats (if Notion allows selective AI add-ons, though typically it's workspace-wide).</li>
                    <li><strong>Compare to standalone AI tools:</strong> If your AI needs are very specific and met by a free standalone tool, that might be more cost-effective initially. However, Notion AI's value is its deep integration.</li>
                </ul>
                <p>Always check the official <a href="https://www.notion.so/pricing" target="_blank">Notion pricing page</a> for the most current details on Notion AI add-on costs.</p>
            """,
            "action_steps": create_list_html([
                ("<strong>Day 1: Activate Trial & Basic Writing.</strong> If available, activate the Notion AI trial. Have team members select a piece of text they've written in Notion and use AI to 'Improve writing' or 'Change tone'. Focus: Basic Editing.", ""),
                ("<strong>Day 2: Summarize & Extract Action Items.</strong> Take a recent long meeting note page. Use Notion AI to 'Summarize' it at the top. Then, try the 'Find action items' feature. Focus: Information Condensing.", ""),
                ("<strong>Day 3: Draft New Content.</strong> On a blank Notion page, ask AI to 'Draft a blog post about [relevant startup topic]' or 'Write 3 subject lines for an email announcing [new feature]'. Focus: First Draft Generation.", ""),
                ("<strong>Day 4-5: Explore AI Blocks & Templates.</strong> Create a new Notion template (e.g., for weekly updates) and incorporate an AI Summary block. Experiment with the 'Custom AI prompt' block for a recurring task. Focus: Workflow Integration.", "")
            ], list_class="action-steps-list", bold_first=False),
            "pros_cons_startup": create_pros_cons_html(
                pros=[
                    ("Seamless Integration: AI lives where your startup's work happens in Notion.", "Contextually Aware: Leverages content on your Notion pages for more relevant AI assistance."),
                    ("Boosts Productivity for Notion Users: Significant time savings on writing, summarizing, and ideation within Notion.", "Encourages Standardization: AI in templates helps maintain consistency in documentation and processes."),
                    ("Relatively Affordable Add-on: If already using Notion, it's a cost-effective way to get integrated AI.")
                ],
                cons=[
                    ("Cost Add-on: It's an additional per-user fee on top of your Notion plan.", "Limited to Notion Environment: Its power is primarily within Notion; less useful for AI tasks outside that ecosystem."),
                    ("Underlying AI Model: May not always be the absolute latest or most powerful model compared to specialized standalone AI tools (though Notion continuously updates).", "Can Lead to Generic Content if Not Guided: Requires good prompting and human refinement for unique brand voice."),
                    ("Usage Limits: Even with the paid add-on, there might be fair use policies or soft limits on very high usage.")
                ]
            ),
            "resources_startup": """
                <ul>
                    <li><a href="https://www.notion.so/help/guides/category/ai" target="_blank" rel="noopener noreferrer">Notion AI Help Guides:</a> Official documentation and tutorials.</li>
                    <li><a href="https://www.notion.so/blog/category/product" target="_blank" rel="noopener noreferrer">Notion Blog (Product Section):</a> For announcements and feature showcases.</li>
                    <li><a href="https://www.youtube.com/@Notion" target="_blank" rel="noopener noreferrer">Notion YouTube Channel:</a> Often has video tutorials on AI features.</li>
                    <li><strong>Notion Community Forums/Groups:</strong> Search for communities on Reddit, Facebook, etc., where users share Notion AI tips and tricks.</li>
                </ul>
            """
        }
    },
    
    # --- Bardeen AI ---
    "bardeen": {
        "name": "Bardeen AI",
        "startup_tagline": "Automate your startup's web-based workflows and repetitive tasks with AI-powered, no-code browser automation.",
        "logo_url": "/static/img/bardeen-logo.png",
        "official_link": "https://www.bardeen.ai/",
        "cta_link": "https://www.bardeen.ai/download",
        "cta_text": "Get Bardeen for Free",
        "sections": {
            "intro_startup": "Why Bardeen AI for Startup Automation?",
            "features_startup": "Key Bardeen AI Features for Streamlining Operations",
            "getting_started_startup": "Getting Started with Bardeen (Browser Extension)",
            "use_cases_startup": "Bardeen in Action: Automating Startup Tasks",
            "integration_startup": "Connecting Your Apps with Bardeen AI",
            "roi_startup": "Bardeen AI's ROI: Time Savings & Process Efficiency",
            "pricing_startup": "Bardeen AI Pricing: Free & Pro Tiers for Startups",
            "action_steps": "Your First Week with Bardeen AI: Quick Wins",
            "pros_cons_startup": "Bardeen AI: Pros & Cons for Startups",
            "resources_startup": "Further Learning & Bardeen Community"
        },
        "content": {
            "intro_startup": """
                <p>Bardeen.ai offers a unique AI-first approach to browser-based automation, allowing startups to automate repetitive web tasks without writing any code. As a browser extension, it can interact with websites you use daily, scrape data, and connect various web apps, all triggered manually or automatically. For startups looking to save time on manual data entry, lead generation, or information gathering from the web, Bardeen can be a powerful ally.</p>
                <p>Startups can leverage Bardeen to:</p>
                <ul>
                    <li><strong>Automate Lead Generation:</strong> Scrape contact information from LinkedIn Sales Navigator, websites, or directories.</li>
                    <li><strong>Streamline Data Entry:</strong> Transfer data between web apps (e.g., from a Typeform submission to a Google Sheet and then to a CRM).</li>
                    <li><strong>Enhance Outreach:</strong> Automate parts of your outreach process by pulling prospect data and drafting personalized messages.</li>
                    <li><strong>Automate Repetitive Web Actions:</strong> Create custom "Playbooks" to perform multi-step actions on websites with a single click.</li>
                </ul>
                <p>Think of it as a Zapier/Make.com alternative that lives in your browser and uses AI to understand webpage context more intuitively for certain automations.</p>
            """,
            "features_startup": create_list_html([
                ("No-Code Automation Builder", "Visually create automation sequences (Playbooks) without writing code."),
                ("AI-Powered Web Scraping", "Extract data from websites, even complex ones, with AI assisting in field detection."),
                ("Contextual AI Commands", "Use natural language to tell Bardeen what to do on the current webpage (e.g., 'scrape all job titles')."),
                ("Pre-built Playbook Marketplace", "Access a library of ready-to-use automations for common tasks and apps."),
                ("Triggers & Schedulers", "Run automations manually, on a schedule, or based on events (e.g., when a new page loads)."),
                ("Integrations with Popular Web Apps", "Connects with Google Sheets, Notion, HubSpot, LinkedIn, Twitter, and many more."),
                ("Browser Extension Based", "Works directly within your Chrome/Edge browser, making it easy to automate tasks as you browse.")
            ], list_class="key-feature-list", bold_first=True),
            "getting_started_startup": """
                <p>Setting up Bardeen for your startup team:</p>
                <ol>
                    <li><strong>Install the Browser Extension:</strong> Visit <a href="https://www.bardeen.ai/" target="_blank">bardeen.ai</a> and install the Chrome (or Edge) extension.</li>
                    <li><strong>Create an Account:</strong> Sign up for a Bardeen account (free tier available).</li>
                    <li><strong>Explore the Interface:</strong>
                        <ul>
                            <li><strong>Bardeen Magic Box (Omnibox):</strong> Press `Cmd/Ctrl + Shift + P` (or your configured shortcut) to open the command palette. This is where you search for Playbooks or give AI commands.</li>
                            <li><strong>Playbook Builder:</strong> Access via the extension icon to create or customize automations.</li>
                            <li><strong>Playbook Marketplace:</strong> Browse and install pre-built automations.</li>
                        </ul>
                    </li>
                    <li><strong>Try a Pre-built Playbook:</strong> Find a simple Playbook from the marketplace that connects two apps you use (e.g., "Save liked tweet to Notion"). Run it to understand the flow.</li>
                    <li><strong>Experiment with Scraping:</strong> Go to a website with listed data (e.g., a directory) and try Bardeen's scraper to extract information into a Google Sheet.</li>
                </ol>
            """,
            "use_cases_startup": """
                <h4>Sales & Lead Generation:</h4>
                <ul>
                    <li><strong>LinkedIn Prospecting:</strong> "When I'm on a LinkedIn Sales Navigator profile, scrape their name, title, company, and save it to my HubSpot CRM."</li>
                    <li><strong>Company Research:</strong> "For a list of company websites in a Google Sheet, visit each site, find the 'Contact Us' page, and extract email addresses."</li>
                </ul>
                <h4>Marketing & Content:</h4>
                <ul>
                    <li><strong>Social Media Monitoring:</strong> "When I find a relevant tweet, save its text, author, and link to a Notion database for content ideas."</li>
                    <li><strong>Content Curation:</strong> "Scrape the headlines and links from the top 10 articles on [news site's specific section] and add them to a Google Sheet."</li>
                </ul>
                <h4>Recruiting & HR:</h4>
                <ul>
                    <li><strong>Candidate Sourcing:</strong> "When viewing a LinkedIn profile that matches my criteria, save their profile URL, name, and experience to an Airtable base."</li>
                    <li><strong>Job Board Monitoring:</strong> "Check [job board URL] daily for new postings with keywords '[your keywords]' and send me a Slack notification." (Requires scheduling)</li>
                </ul>
                <h4>Productivity & Operations:</h4>
                <ul>
                    <li><strong>Meeting Preparation:</strong> "For upcoming Google Calendar events, find the LinkedIn profiles of all attendees and save them to a Notion page."</li>
                    <li><strong>Data Transfer:</strong> "When a new row is added to this Google Sheet, create a corresponding task in Asana."</li>
                </ul>
            """,
            "integration_startup": """
                <p>Bardeen AI integrates with a wide range of popular web applications that startups frequently use. Its integration model is primarily action-based, performing tasks within these apps via its browser extension capabilities or direct API connections where available.</p>
                <p>Key integration categories for startups:</p>
                <ul>
                    <li><strong>CRMs:</strong> HubSpot, Salesforce (often via scraping or specific playbooks), Pipedrive.</li>
                    <li><strong>Communication & Collaboration:</strong> Slack, Gmail, Google Calendar, Notion, Airtable, Google Sheets, Coda.</li>
                    <li><strong>Social Media & Professional Networks:</strong> LinkedIn (including Sales Navigator), Twitter/X.</li>
                    <li><strong>Productivity Tools:</strong> Asana, Trello, ClickUp.</li>
                    <li><strong>Data Sources:</strong> Various websites for scraping, Google Search.</li>
                    <li><strong>Generic Webhooks & APIs:</strong> For more custom integrations, Bardeen often supports sending data to webhooks or making basic API calls as part of a Playbook.</li>
                </ul>
                <p><strong>How Integrations Work:</strong></p>
                <ul>
                    <li><strong>Browser Context:</strong> Bardeen often uses the fact that you are logged into an app in your browser to perform actions on your behalf.</li>
                    <li><strong>Official APIs (when available):</strong> For some core apps, Bardeen may use official APIs for more robust data transfer.</li>
                    <li><strong>Scraping:</strong> For apps without direct integration or for pulling public data, Bardeen's AI-powered scraper is key.</li>
                </ul>
                <p><strong>Startup Advantage:</strong> Bardeen can help "glue" together web apps that might not have native integrations, especially for tasks involving data extraction from one site and input into another, without complex API coding.</p>
            """,
            "roi_startup": """
                <p>For startups, Bardeen AI's ROI is primarily driven by significant time savings on manual, repetitive web-based tasks:</p>
                <ul>
                    <li><strong>Reduced Manual Data Entry & Scraping:</strong> Automating the collection of sales leads, market research data, or contact information can save dozens of hours per month.
                        <ul><li><em>Example:</em> If a sales development rep (SDR) spends 5 hours/week manually collecting leads, and Bardeen automates 80% of that, it's 4 hours/week saved.</li></ul>
                    </li>
                    <li><strong>Increased Efficiency in Outreach & Prospecting:</strong> By automating parts of the research and data gathering for outreach, sales and marketing teams can focus more on actual engagement.</li>
                    <li><strong>Faster Information Gathering:</strong> Quickly compile data from multiple web sources for competitive analysis, content creation, or due diligence.</li>
                    <li><strong>Improved Data Accuracy:</strong> Automation can reduce human errors common in manual data transfer.</li>
                    <li><strong>Empowering Non-Technical Users:</strong> Allows team members without coding skills to build their own automations, freeing up developer resources for core product work.</li>
                </ul>
                <p><strong>Measuring ROI:</strong>
                    Estimate the time spent on specific repetitive web tasks before Bardeen.
                    Track how many of these tasks are automated and the time now taken (often just seconds for a Playbook run).
                    Calculate the value of the time saved based on employee costs.
                    Monitor any increase in output (e.g., number of leads processed, articles researched) due to automation.
                </p>
            """,
            "pricing_startup": """
                <p>Bardeen AI typically offers a tiered pricing model, including a generous free plan suitable for startups to begin with:</p>
                <ul>
                    <li><strong>Free Plan:</strong>
                        <ul>
                            <li>Usually includes a certain number of free Playbook runs or AI credits per month.</li>
                            <li>Access to most core features and many pre-built Playbooks.</li>
                            <li>May have limitations on the number of custom Playbooks or certain premium integrations/actions.</li>
                            <li><strong>Best for:</strong> Individual users, very early-stage startups testing automation, or light usage.</li>
                        </ul>
                    </li>
                    <li><strong>Pro/Premium Plan(s):</strong>
                        <ul>
                            <li>Priced per user per month (e.g., $10-$29/user/month, with discounts for annual billing).</li>
                            <li>Significantly more Playbook runs or AI credits.</li>
                            <li>Access to all integrations and premium actions (e.g., deeper AI capabilities, more complex Playbook logic).</li>
                            <li>Features like scheduling, parallel runs, and potentially team collaboration features.</li>
                            <li><strong>Best for:</strong> Startups actively using automation in daily workflows, needing higher volumes, or requiring premium features. Good for sales teams, marketers, or operations roles relying on web automation.</li>
                        </ul>
                    </li>
                    <li><strong>Team/Business Plans (if available):</strong>
                        <ul>
                            <li>May offer bulk pricing, centralized billing, and team management features for larger startup teams.</li>
                        </ul>
                    </li>
                </ul>
                <p><strong>Startup Strategy:</strong>
                    Start every team member on the Free plan to explore its capabilities.
                    Identify power users or critical automations that hit free tier limits or require Pro features, then upgrade those users.
                    Bardeen's per-user cost for Pro is generally competitive for the time it can save, making it a strong ROI proposition even for smaller teams if used effectively.
                </p>
                <p>Always check the official <a href="https://www.bardeen.ai/pricing" target="_blank">Bardeen pricing page</a> for the latest details and feature comparisons between plans.</p>
            """,
            "action_steps": create_list_html([
                ("<strong>Day 1: Install & Run a Pre-built Playbook.</strong> Install the Bardeen extension. Browse the marketplace for a simple Playbook connecting two apps you use (e.g., 'Save a Tweet to Notion'). Run it. Focus: Understanding Basic Automation.", ""),
                ("<strong>Day 2: Basic Web Scraping.</strong> Go to a simple list-based website (e.g., a blog's front page). Use Bardeen's scraper (`Cmd/Ctrl+Shift+S` or right-click menu) to try and extract titles and links into a Google Sheet. Focus: Data Extraction.", ""),
                ("<strong>Day 3: Automate a Repetitive Click.</strong> Identify a task where you always click the same 2-3 buttons on a specific website. Try to build a very simple custom Playbook to automate those clicks. Focus: Custom Action.", ""),
                ("<strong>Day 4-5: Tackle a Startup Pain Point.</strong> Pick a minor but annoying repetitive web task your startup faces (e.g., copying info from LinkedIn to a spreadsheet). Dedicate time to finding or building a Bardeen Playbook for it. Focus: Solving a Real Problem.", "")
            ], list_class="action-steps-list", bold_first=False),
            "pros_cons_startup": create_pros_cons_html(
                pros=[
                    ("No-Code Browser Automation: Empowers non-technical users to automate web tasks.", "AI-Powered Scraping & Context: Can often understand webpage structure better than traditional scrapers."),
                    ("Generous Free Tier: Excellent for startups to get started and see value.", "Quick to Set Up & Use: Browser extension makes it very accessible."),
                    ("Growing Playbook Marketplace: Many pre-built solutions for common tasks.")
                ],
                cons=[
                    ("Browser-Dependent: Primarily automates tasks within the browser; less suited for desktop or complex backend automation (compared to Zapier/Make for server-side).", "Can Be Fragile if Website Structures Change: Automations relying on specific HTML structures can break if sites are updated (though AI helps mitigate this).", "Learning Curve for Complex Playbooks: Building highly custom or conditional automations can take time to master."),
                    ("Resource Intensive: Browser extensions, especially those actively interacting with pages, can sometimes consume browser resources.", "Scalability for Very High Volumes: For extremely high-volume server-to-server automation, dedicated platforms might be more robust.")
                ]
            ),
            "resources_startup": """
                <ul>
                    <li><a href="https://www.bardeen.ai/learn" target="_blank" rel="noopener noreferrer">Bardeen Learning Hub:</a> Official tutorials, guides, and use cases.</li>
                    <li><a href="https://www.bardeen.ai/playbooks" target="_blank" rel="noopener noreferrer">Bardeen Playbook Marketplace:</a> Explore pre-built automations.</li>
                    <li><a href="https://www.youtube.com/@BardeenAI" target="_blank" rel="noopener noreferrer">Bardeen YouTube Channel:</a> Video tutorials and demos.</li>
                    <li><a href="https://www.bardeen.ai/community" target="_blank" rel="noopener noreferrer">Bardeen Community (if available, often Slack or Discord):</a> Connect with other users, get help, and share ideas.</li>
                </ul>
            """
        }
    }
}

@app.route('/')
def index():
    # Pass tools_data to index if you want to list them there dynamically as well
    return render_template('index.html', tools_data=tools_data)

@app.route('/bard')
def bard():
    return render_template('bard.html', tool_data=tools_data['bard'])

@app.route('/chatgpt')
def chatgpt():
    return render_template('chatgpt.html', tool_data=tools_data['chatgpt'])

@app.route('/claude')
def claude():
    return render_template('claude.html', tool_data=tools_data['claude'])

@app.route('/gemini')
def gemini():
    return render_template('gemini.html', tool_data=tools_data['gemini'])

@app.route('/notionai')
def notionai():
    return render_template('notionai.html', tool_data=tools_data['notionai'])

@app.route('/bardeen')
def bardeen():
    return render_template('bardeen.html', tool_data=tools_data['bardeen'])

if __name__ == '__main__':
    # Get the port from the environment variable Render sets, default to 5000 for local
    port = int(os.environ.get("PORT", 5000)) 
    # Run on 0.0.0.0 to be accessible. Set debug to False for a pseudo-production local test
    app.run(debug=False, host='0.0.0.0', port=port)
