# GDSC 8 Tutorial Specifications

This document contains detailed specifications for each tutorial in the Global Data Science Challenge 8: Green Agents of Change.

## Tutorial Structure Overview

1. **Tutorial 1**: Joining the Challenge ✅ (Complete)
2. **Tutorial 2**: Data Exploration and Your First API Call
3. **Tutorial 3**: Your First Submission
4. **Tutorial 4**: Building Real LLM-Based Matching
5. **Tutorial 5**: Advanced Techniques and Best Practices
6. **Final Module**: GenAI Consulting Best Practices

---

## Tutorial 1: Joining the Challenge 
*Learn how to create an account, register for the competition, and understand the rules and objectives.*

**Status**: Complete - no changes needed
**Content**: Account setup, team formation, AWS access, Mistral API setup
**Learning Outcome**: Participants can access all platforms and are ready to code

---

## Tutorial 2: Data Exploration and Your First API Call
*Understanding the challenge data and making your first Mistral API call*

### Learning Objectives
- Download and explore the job/training dataset
- Make your first Mistral API call with cost tracking
- Understand tokens, models, and pricing
- Apply basic data filtering and batching techniques

### Module Structure

#### 2.1 Understanding the Challenge Data
- **Data Download**: AWS S3 data retrieval (200 jobs, 467 trainings)
- **Data Structure**: Jobs vs trainings format differences
- **Scale Awareness**: 697 items × multiple personas = cost considerations
- **Real-world Context**: Career matching at scale

> **Author Note**: Include high-level statistics and breakdowns (e.g., jobs by domain, training by level). Add exercises that encourage participants to explore data patterns beyond just loading it.

#### 2.2 Your First Mistral API Call
- **Environment Setup**: Libraries and API key configuration
- **What is a Token?**: Understanding the fundamental unit of LLM processing
- **Model Comparison**: Small vs large models (cost, speed, quality)
- **First API Call**: Simple prompt with cost calculation
- **Best Practice**: Always start with the smallest model that works

> **Author Note**: Emphasize concrete cost calculations for at least 2 different Mistral models (e.g., mistral-7b vs mistral-large). Show actual token counts and costs for identical prompts to make the trade-offs tangible.

#### 2.3 Data Exploration with LLMs
- **Job Analysis**: Extract key information using LLMs
- **Training Analysis**: Understand skill development paths
- **Basic Filtering**: Use LLMs for categorization (e.g., seniority levels)
- **Caching Strategy**: Process data once, reuse efficiently

#### 2.4 Hands-on Exercises
- Explore job and training examples
- Calculate tokens and costs for different approaches
- Build a simple data categorization system
- Compare small vs large model performance

**Key Outcome**: Participants understand the data and can effectively use the Mistral API

---

## Tutorial 3: Your First Submission
*Get on the leaderboard fast - submit a simple solution and understand the scoring system*

### Learning Objectives
- Create the simplest possible valid submission
- Navigate the submission process step-by-step
- Understand evaluation criteria and scoring
- See your name on the leaderboard!

### Module Structure

#### 3.1 The Simplest Solution
- **Minimal Viable Submission**: Same job recommendation for everyone
- **JSONL Format**: Understanding the submission structure
- **Code Walkthrough**: 10 lines that create a valid submission
- **Why This Matters**: Get comfortable with the process before optimizing

#### 3.2 Submission Process
- **Step-by-Step**: From code to uploaded solution
- **File Formatting**: Proper JSONL structure
- **Upload Mechanism**: Platform navigation
- **Confirmation**: How to verify your submission

#### 3.3 Understanding Evaluation
- **Scoring System**: How points are calculated
- **Hard Filters**: Job matching requirements that must be met
- **Training Progression**: Basic → Intermediate → Advanced logic
- **Edge Cases**: Age restrictions and awareness classifications

#### 3.4 Your Score Analysis
- **Reading Results**: What your score means
- **Baseline Comparison**: How you rank against simple solutions
- **Improvement Opportunities**: What the scoring system rewards

#### 3.5 Iterate Immediately
- **Quick Win**: Improve your simple solution
- **A/B Testing**: Try different approaches and compare scores
- **Leaderboard Strategy**: Understanding competitive positioning

> **Author Note**: Establish the test-improve cycle as a core methodology. Show how to systematically compare submissions, track what works, and build on successes. This pattern should carry through all subsequent tutorials.

**Key Outcome**: Participants have submitted a solution and understand how to improve their score

---

## Tutorial 4: Building Real LLM-Based Matching
*Create a competitive solution using persona conversations and intelligent matching*

### Learning Objectives
- Implement persona conversation systems
- Extract structured information from conversations
- Build LLM-based job/training matching
- Generate competitive JSONL submissions

### Module Structure

#### 4.1 Persona Conversation System
- **Conversation Flow**: Multi-turn interactions with personas
- **Information Extraction**: Name, skills, location, preferences, experience
- **Structured Output**: Convert conversations to usable data
- **Error Handling**: Robust conversation management

#### 4.2 Intelligent Matching Algorithm
- **Job Matching**: Skills, location, and experience alignment
- **Training Recommendations**: Gap analysis and skill progression
- **Multi-criteria Decision Making**: Balancing multiple factors
- **Edge Case Handling**: Age restrictions and awareness cases

#### 4.3 End-to-End Implementation
- **Complete Pipeline**: Conversations → Extraction → Matching → Submission
- **Batch Processing**: Handle multiple personas efficiently
- **Quality Assurance**: Test your logic before submitting
- **Performance Optimization**: Balance quality and cost

#### 4.4 Advanced Matching Strategies
- **Pre-processing**: Extract job/training metadata once
- **Filtering Pipeline**: Multi-stage matching for efficiency
- **Model Selection**: When to use small vs large models
- **Caching Strategies**: Reuse processed information

#### 4.5 Competitive Analysis
- **Score Comparison**: Simple vs LLM-based approaches
- **Cost Analysis**: Token usage and efficiency
- **Quality Assessment**: Matching accuracy improvements
- **Iteration Strategy**: Systematic improvement approach

> **Author Note**: Incorporate explicit coverage of GDSC 8's hard filter requirements (seniority, location, skills coverage ≥70%) and Brazilian green jobs context. Show how LLM matching can handle these constraints effectively.

**Key Outcome**: Participants have a competitive LLM-based solution and understand optimization techniques

---

## Tutorial 5: Advanced Techniques and Best Practices
*Level up your solution with better prompts, LLM-assisted development, and professional optimization strategies*

### Learning Objectives
- Master advanced prompt engineering techniques
- Use LLMs as development assistants effectively
- Implement sophisticated matching strategies
- Apply professional GenAI development practices

### Module Structure

#### 5.1 Advanced Prompt Engineering
- **Prompt Optimization**: Chain-of-thought, few-shot examples
- **Context Management**: Efficient use of limited context windows
- **Structured Output**: Getting reliable JSON/formatted responses
- **Multi-turn Conversations**: Managing complex interactions

#### 5.2 LLMs as Development Partners
- **Claude/Copilot Integration**: Using AI to write and review code
- **Code Generation**: Effective prompts for quality code
- **Debugging**: AI-assisted troubleshooting and optimization
- **Quality Assessment**: When to trust AI vs manual verification

#### 5.3 Sophisticated Matching Strategies
- **Agent-to-Agent Communication**: Interviewer ↔ Matcher real-time collaboration
- **Dynamic Filtering**: Adaptive matching based on persona complexity
- **Multi-model Ensembles**: Combining different models for better results
- **Semantic Understanding**: Beyond keyword matching

#### 5.4 Performance and Cost Optimization
- **Model Selection Strategy**: Right model for each task
- **Batching and Parallelization**: Efficient processing patterns  
- **Caching Strategies**: Memory vs computation trade-offs
- **Token Management**: Minimize costs without sacrificing quality

#### 5.5 Professional Development Practices
- **Code Organization**: Clean, maintainable GenAI solutions
- **Testing Strategies**: Validating LLM-based systems
- **Version Control**: Managing prompt and model iterations
- **Documentation**: Explaining AI-driven decision making

#### 5.6 Competition-Winning Strategies
- **Edge Case Mastery**: Handling unusual personas and requirements
- **Quality vs Speed**: Optimization for competitive advantage
- **Continuous Improvement**: Systematic experimentation approach
- **Leaderboard Analysis**: Learning from top solutions

**Key Outcome**: Participants have advanced skills for building professional-grade GenAI solutions

---

## Final Module: GenAI Consulting Best Practices 
*Professional-grade strategies for real-world client projects*

### Learning Objectives
- Synthesize learnings into professional frameworks
- Understand enterprise deployment considerations
- Develop client communication strategies for AI projects
- Create reusable methodologies for future projects

### Module Structure

#### 6.1 The Professional Framework
- **Discovery Process**: Understanding client AI readiness
- **Solution Architecture**: Scalable, maintainable design patterns
- **Risk Assessment**: Technical, financial, and business risks
- **Success Metrics**: Defining and measuring AI project success

#### 6.2 Client Communication Strategies
- **Technical Translation**: Explaining AI concepts to business stakeholders
- **Cost Justification**: ROI frameworks for AI investments
- **Change Management**: Helping organizations adopt AI solutions
- **Expectation Setting**: Realistic timelines and capabilities

#### 6.3 Enterprise Deployment
- **Scaling Considerations**: From prototype to production
- **Security and Compliance**: Enterprise AI requirements
- **Integration Patterns**: Fitting AI into existing systems
- **Monitoring and Maintenance**: Long-term solution health

#### 6.4 Reusable Methodologies
- **Solution Templates**: Accelerate future projects
- **Decision Frameworks**: Model selection, architecture choices
- **Cost Optimization Playbooks**: Proven strategies for efficiency
- **Quality Assurance**: Testing and validation approaches

**Key Outcome**: Participants have professional-grade methodologies for client AI projects

---

## Implementation Notes

### Progressive Complexity
The tutorials follow a deliberate progression:
- **Tutorial 2**: Understand the problem and tools
- **Tutorial 3**: Submit fast, get feedback
- **Tutorial 4**: Build something competitive
- **Tutorial 5**: Optimize and professionalize
- **Final Module**: Apply to real-world consulting

### Key Teaching Philosophy
1. **Immediate submission focus** - Get on the leaderboard by Tutorial 3
2. **Test-improve cycle** - Continuous iteration based on real feedback
3. **Cost awareness** - Always consider token usage and efficiency
4. **Practical focus** - Real code, real submissions, real scores
5. **Green computing** - Optimize for both performance and environmental impact