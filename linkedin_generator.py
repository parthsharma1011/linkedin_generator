import json
import os
from typing import Dict, List
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

load_dotenv()

class LinkedInPostGenerator:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # Initialize Tavily client
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # Create agents
        self.research_agent = self.create_research_agent()
        self.writer_agent = self.create_writer_agent()
        self.validator_agent = self.create_validator_agent()
    
    def create_research_agent(self):
        return Agent(
            role="Research Specialist",
            goal="Find relevant, recent data and trends to support compelling LinkedIn posts",
            backstory="Expert researcher who finds credible statistics, trends, and angles to make posts timely and authoritative.",
            llm=self.llm,
            verbose=True
        )
    
    def create_writer_agent(self):
        return Agent(
            role="LinkedIn Content Writer",
            goal="Create engaging LinkedIn posts that drive engagement and build thought leadership",
            backstory="Professional copywriter specializing in LinkedIn content with deep understanding of platform best practices.",
            llm=self.llm,
            verbose=True
        )
    
    def create_validator_agent(self):
        return Agent(
            role="Content Quality Validator",
            goal="Ensure posts are accurate, authentic, and optimized for LinkedIn engagement",
            backstory="Quality assurance expert who catches inaccuracies, clichés, and ensures professional authenticity.",
            llm=self.llm,
            verbose=True
        )
    
    def research_topic(self, topic: str, post_type: str) -> Dict:
        """Research topic using Tavily API"""
        try:
            # Create focused search queries
            queries = [
                f"{topic} statistics 2024",
                f"{topic} trends recent news",
                f"{topic} expert opinions insights"
            ]
            
            research_data = {
                "topic": topic,
                "key_facts": [],
                "trending_angles": [],
                "sources": []
            }
            
            for query in queries:
                response = self.tavily.search(
                    query=query,
                    search_depth="basic",
                    max_results=3
                )
                
                for result in response.get("results", []):
                    research_data["sources"].append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", "")[:200]
                    })
            
            return research_data
            
        except Exception as e:
            print(f"Research failed: {e}")
            return {"topic": topic, "key_facts": [], "trending_angles": [], "sources": []}
    
    def create_research_task(self, topic: str, post_type: str, research_data: Dict):
        return Task(
            description=f"""Analyze research data and extract key insights for a LinkedIn post.

TOPIC: {topic}
POST TYPE: {post_type}

RESEARCH DATA:
{json.dumps(research_data, indent=2)}

Extract and return JSON:
{{
    "key_facts": ["3-5 compelling statistics or facts"],
    "trending_angles": ["2-3 current angles or perspectives"],
    "credible_sources": ["sources that can be referenced"],
    "hook_opportunities": ["potential opening lines based on research"]
}}

Focus on recent, credible information that supports the topic.""",
            agent=self.research_agent,
            expected_output="JSON with research insights"
        )
    
    def create_writing_task(self, topic: str, tone: str, post_type: str, research_insights: str):
        return Task(
            description=f"""Write a compelling LinkedIn post using the research insights.

TOPIC: {topic}
TONE: {tone}
POST TYPE: {post_type}

RESEARCH INSIGHTS:
{research_insights}

POST STRUCTURE GUIDELINES:
- Story: Hook → Personal anecdote → Lesson → CTA
- Hot take: Contrarian hook → Reasoning → Invite discussion  
- Announcement: News → Why it matters → Next steps
- Lesson learned: Challenge → What happened → Takeaway

LINKEDIN BEST PRACTICES:
- Strong first line (hook)
- Short paragraphs (1-2 sentences)
- Line breaks for readability
- Include relevant statistics naturally
- End with engagement driver (question/CTA)
- 150-300 words optimal

Return JSON:
{{
    "post_content": "the complete LinkedIn post",
    "hook": "first line extracted",
    "word_count": "number",
    "facts_used": ["research points incorporated"]
}}""",
            agent=self.writer_agent,
            expected_output="JSON with LinkedIn post content"
        )
    
    def create_validation_task(self, post_content: str, research_insights: str, tone: str):
        return Task(
            description=f"""Validate the LinkedIn post for quality, accuracy, and authenticity.

POST CONTENT:
{post_content}

ORIGINAL RESEARCH:
{research_insights}

EXPECTED TONE: {tone}

VALIDATION CHECKLIST:
1. Accuracy: Do claims match research data?
2. Authenticity: Does it sound genuine, not robotic?
3. Engagement: Is the hook compelling?
4. LinkedIn clichés: Flag overused phrases
5. Tone consistency: Matches requested tone?
6. Structure: Proper formatting and flow?

CRINGE FLAGS TO AVOID:
- "I'm humbled to announce..."
- "Excited to share..."
- Generic motivational quotes
- Excessive self-promotion

Return JSON:
{{
    "validation_passed": true/false,
    "score": "1-10 rating",
    "accuracy_issues": ["any factual problems"],
    "quality_issues": ["areas for improvement"],
    "cringe_flags": ["cliché phrases found"],
    "suggestions": ["specific improvements"],
    "final_verdict": "ready to post / needs revision"
}}""",
            agent=self.validator_agent,
            expected_output="JSON validation report"
        )
    
    def generate_post(self, topic: str, tone: str = "professional", post_type: str = "thought-leader"):
        print(f"Generating LinkedIn post about: {topic}")
        print(f"Tone: {tone} | Type: {post_type}")
        print("-" * 50)
        
        # Step 1: Research
        print("Step 1: Researching topic...")
        research_data = self.research_topic(topic, post_type)
        
        research_task = self.create_research_task(topic, post_type, research_data)
        research_crew = Crew(
            agents=[self.research_agent],
            tasks=[research_task],
            process=Process.sequential,
            verbose=False
        )
        
        research_result = research_crew.kickoff()
        print("Research completed")
        
        # Step 2: Write post
        print("Step 2: Writing post...")
        writing_task = self.create_writing_task(topic, tone, post_type, str(research_result))
        writing_crew = Crew(
            agents=[self.writer_agent],
            tasks=[writing_task],
            process=Process.sequential,
            verbose=False
        )
        
        writing_result = writing_crew.kickoff()
        print("Writing completed")
        
        # Parse writing result
        try:
            result_str = str(writing_result)
            if '```json' in result_str:
                result_str = result_str.split('```json')[1].split('```')[0].strip()
            elif '```' in result_str:
                result_str = result_str.split('```')[1].split('```')[0].strip()
            
            post_data = json.loads(result_str)
        except Exception as e:
            print(f"Failed to parse writing result: {e}")
            return None
        
        # Step 3: Validate
        print("Step 3: Validating post...")
        validation_task = self.create_validation_task(
            post_data.get("post_content", ""),
            str(research_result),
            tone
        )
        validation_crew = Crew(
            agents=[self.validator_agent],
            tasks=[validation_task],
            process=Process.sequential,
            verbose=False
        )
        
        validation_result = validation_crew.kickoff()
        print("Validation completed")
        
        # Parse validation result
        try:
            result_str = str(validation_result)
            if '```json' in result_str:
                result_str = result_str.split('```json')[1].split('```')[0].strip()
            elif '```' in result_str:
                result_str = result_str.split('```')[1].split('```')[0].strip()
            
            validation_data = json.loads(result_str)
        except Exception as e:
            print(f"Failed to parse validation result: {e}")
            validation_data = {"validation_passed": False, "score": 0}
        
        return {
            "post": post_data,
            "validation": validation_data,
            "research_sources": len(research_data.get("sources", []))
        }

def main():
    generator = LinkedInPostGenerator()
    
    print("LinkedIn Post Generator")
    print("=" * 30)
    
    # Get user input
    topic = input("Enter your topic/idea: ").strip()
    if not topic:
        print("Topic is required!")
        return
    
    print("\nTone options: professional, casual, thought-leader")
    tone = input("Select tone (default: professional): ").strip() or "professional"
    
    print("\nPost types: story, hot-take, announcement, lesson-learned")
    post_type = input("Select post type (default: thought-leader): ").strip() or "thought-leader"
    
    # Generate post
    result = generator.generate_post(topic, tone, post_type)
    
    if result:
        print("\n" + "="*60)
        print("GENERATED LINKEDIN POST")
        print("="*60)
        print(result["post"]["post_content"])
        print("\n" + "-"*60)
        
        print(f"Word count: {result['post'].get('word_count', 'N/A')}")
        print(f"Validation score: {result['validation'].get('score', 'N/A')}/10")
        print(f"Research sources used: {result['research_sources']}")
        
        if result["validation"].get("suggestions"):
            print(f"\nSuggestions:")
            for suggestion in result["validation"]["suggestions"]:
                print(f"  - {suggestion}")
        
        print(f"\nStatus: {result['validation'].get('final_verdict', 'Unknown')}")
    else:
        print("Failed to generate post. Please try again.")

if __name__ == "__main__":
    main()