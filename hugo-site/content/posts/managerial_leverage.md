---
title: "Managerial Leverage with AI Agents"
date: 2026-04-25
description: "Applying Andy Grove's High Output Management to managing AI agents: limiting steps, task-relevant maturity, and managerial leverage."
aliases: ["/p/managerial_leverage.html"]
---



# Managerial Leverage with AI Agents


##### <time datetime="2026-04-25">April 25th, 2026</time>


In _High Output Management_, Andy Grove argues that a manager's actions need to have leverage to improve a manager's output. In the world of 1983 when Grove wrote his book, high-leverage management activities could be achieved only through managing other employees.


With the increase in agentic AI capabilities, managing AI agents is becoming another high leverage activity. And Grove's insights help us become more efficient managers of AI agents.


---


A key step in making a process more efficient is identifying its limiting step. In _High Output Management_, Grove has an example of a breakfast factory where the limiting step is boiling eggs. While toasting bread and pouring coffee are quick steps, the whole breakfast cannot be completed until the eggs are boiled which takes the longest out of all steps. Hence, the breakfast factory production flow should be designed by starting with the longest (or most difficult, or most sensitive, or most expensive) step and working back to other parts of the production process.


Given the speed of development possible with AI agents, the limiting step is _you_. Hence, the AI production flow should be designed with you being the limiting step in mind. Any time you see yourself manually spending time on any task, you should ask yourself whether your contribution is truly necessary or whether it could be automated using rules, hooks, guardrails, etc.


For instance, perhaps you are finding yourself spending time manually approving commands. While the command approval itself takes at most a few seconds, it is a limiting step because the agents cannot run until you approve the command. To solve this limiting step, you should set up an environment where you are comfortable using `--dangerously-skip-permissions`. That might involve installing Jeffrey Emmanuel's [Destructive Command Guard](https://github.com/Dicklesworthstone/destructive_command_guard) to prevent the execution of destructive commands. Alternatively, you might set up a special environment without access to prod, so agents' mistakes would not affect your product's end users.


---


Another limiting step might be agents consistently making similar mistakes that you then need to spend significant time fixing. While you can easily blame agents for their lack of accuracy (and be correct), blaming won't solve your issues. As Grove argues:


> A manager's most important responsibility is to elicit top performance from his subordinates.


If you don't elicit top performance from your agents, it is your failure as their manager. Grove argues that a key component of subordinates' performance is task-relevant maturity (TRM). If someone joins your company straight out of college, their TRM for almost all tasks is very low. Hence, they require close supervision with structured explanation of "what," "when," and "how." As your subordinates' TRM increases, you give fewer direct instructions and more support, mutual reasoning, and eventually have minimal involvement. This is similar for agents. When an agent's TRM is low due to either lackluster base model capabilities or low customization for your workflow/codebase, you need to carefully review the agents' work. Once your agents' TRM increases, you trust them to complete complex tasks well with intermittent monitoring. The increased TRM is often recorded in `AGENTS.md` files and in skills.


Let's assume your agents' TRM is low. There are many ways you could increase their TRM.


If your agent constantly produces UI bugs, you could mandate that an agent build your website/app locally and verify through screenshots that there are no UI issues. But also remember that agents are lazy, and simply saying "you must review your work" is insufficient to ensure quality outputs. A more effective approach would be to create a quality control checklist an agent needs to satisfy, and then mandate that an agent explicitly affirm that all checklist steps were completed in its output. Another option is writing a series of comprehensive tests that need to successfully pass before an agent can commit their work.


If the issues are more stylistic/textual rather than structural, then you should encode your best practices into skills and easily queryable data sources. As you are the limiting step in getting agents to work, you need to continually redesign your coding process such that you minimize the number of tasks where lack of your input blocks progress. The time you spend improving your workflows allows the agents to work more autonomously in the future. That is managerial leverage.


---


Even with high TRM, agents will sometimes go off-target. In those cases, you should remember Grove's saying that "it is better to catch a bad raw egg than a cooked one." In more formal wording, "to get acceptable quality at the lowest cost, it is vitally important to reject defective material at a stage where its accumulated value is at the lowest possible level." For agents, this means quickly discarding code or conversations where an agent has gone off-target. It is a much more effective use of tokens to revert code changes, improve your original prompt, and start a new conversation rather than trying to salvage the original conversation.


---


A typical workflow of a software engineer now involves simultaneously managing a handful of AI agents and switching between them. You might find that the limiting step for prompting agents is your typing speed. If that is the case, then you should consider using voice dictation solutions like Wispr Flow.


A lot of process limiting steps are worth automating away, but cognitive limiting steps are a valuable source of insight that turns into leverage. Thus, you should be wary of sacrificing quality for speed. If you very quickly give your subordinate a vague task, they might spend significant time exploring different approaches but none of them would be what you originally envisioned. Well-defined tasks allow subordinates to efficiently complete them. Using voice dictation usually means prioritizing speed and in-the-moment thinking when defining tasks for agents. But defining a task well requires intentional thought and one of the best ways to think is through writing. Grove cautions that both too few and too many subordinates reduce a manager's leverage:


> An important component of managerial leverage is the number of subordinates a manager has. If he does not have enough, his leverage is obviously reduced. If he has too many, he gets bogged down—with the same result.


It is obvious when you have too few subordinates and thus too little leverage: you have a lot of free time that is not used for other projects important for the firm. A less obvious insight from Grove is that attempting to maximize the number of your subordinates leads to suboptimal results. If you always use voice dictation with the goal of increasing your speed without reflecting on what is important for each task you give an agent, some details are bound to slip by; slop will begin to accumulate. Efficient use of subordinates requires a manager's thoughtfulness. For instance, using voice dictation to tell an agent to move a button is perfectly reasonable. However, telling an agent to implement a major refactor without considering trade-offs of different architectural choices is a less effective use of voice dictation.


Leverage comes from actions where a manager carefully weighs the value of speed against thoughtfulness. As Grove said:


> A manager must keep many balls in the air at the same time and shift his energy and attention to activities that will most increase the output of his organization. In other words, he should move to the point where his _leverage_ will be the greatest.


---


You are a manager of agents now. Start acting like one.


---


<iframe src="https://maksymsherman.substack.com/embed" style="border:1px solid #434343; background:#252525; width: 100%; max-width: 480px; height: 320px; display: block; margin: 0 auto;" frameborder="0" scrolling="no">
</iframe>
