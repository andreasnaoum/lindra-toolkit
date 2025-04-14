# Define different personas to test each aspect of the assistant
personas = [
    {
        "name": "Leo",
        "age": 34,
        "pain_type": "Mild lower back discomfort from desk job",
        "duration": "1 year",
        "psychological_profile": "Pragmatic, solution-focused, minimal distress",
        "test_category": "Activity Modification",
        "specific_focus": "Ergonomics and movement breaks",
        "communication_style": "Direct and practical",
        "prompt_insights": "Leo experiences mild back discomfort after long days at his computer. It doesn't significantly impact his life, but he's noticed it's becoming more frequent. He doesn't catastrophize about his pain but tends to ignore early warning signs until discomfort forces him to take a break. He's looking for practical solutions he can implement in his workday. He would benefit from ergonomic advice, simple stretches, and structured movement breaks."
    },
    {
        "name": "Aisha",
        "age": 30,
        "pain_type": "Occasional knee pain from old sports injury",
        "duration": "3 years",
        "psychological_profile": "Active lifestyle, some uncertainty about limits",
        "test_category": "Activity Pacing",
        "specific_focus": "Balancing activity and rest",
        "communication_style": "Enthusiastic and curious",
        "prompt_insights": "Aisha experiences knee pain when she pushes too hard in her recreational sports and fitness activities. She has a positive relationship with exercise but sometimes struggles to find the right balance between staying active and avoiding pain flares. She doesn't avoid physical activity but occasionally overdoes it, resulting in several days of discomfort. She would benefit from practical pacing strategies and learning to recognize her body's signals before pain becomes significant."
    },
    {
        "name": "Ethan",
        "age": 35,
        "pain_type": "Chronic low back pain from herniated disc",
        "duration": "4 years",
        "psychological_profile": "Negative core beliefs, identity disruption, perfectionism",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Addressing core beliefs",
        "communication_style": "Reflective and self-critical",
        "prompt_insights": "Ethan's pain has fundamentally altered his core beliefs about himself. He previously defined himself through physical capability and career success. Now he believes he is 'broken,' 'a burden to others,' and 'will never be whole again.' He sees himself as fundamentally damaged and unworthy of the same respect he once received. He judges himself harshly for not recovering and has developed perfectionist standards for other areas of life to compensate. His worth is tied to productivity, and he struggles with profound identity loss. He would benefit from identifying these core beliefs, understanding their impact on his pain experience and behaviors, and working to develop more balanced and compassionate self-beliefs."
    },
    {
        "name": "Nadia",
        "age": 29,
        "pain_type": "Migraine headaches",
        "duration": "7 years",
        "psychological_profile": "Control-focused core beliefs, hypervigilance, self-blame",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Challenging control beliefs",
        "communication_style": "Precise, analytical, information-seeking",
        "prompt_insights": "Nadia holds deep core beliefs about control and responsibility. She believes 'If I can't control my pain, I can't control anything in my life,' and 'I should be able to overcome this through sheer determination.' She constantly monitors her body for signs of an impending migraine and blames herself when attacks occur, believing she must have done something wrong or failed to prevent it. She researches extensively and tries numerous treatments, viewing each failure as personal inadequacy rather than the complex nature of migraines. She needs help recognizing how these control-focused core beliefs increase her stress, perpetuate hypervigilance, and ultimately worsen her pain condition."
    },
    {
        "name": "Marcus",
        "age": 33,
        "pain_type": "Widespread fibromyalgia pain",
        "duration": "3 years",
        "psychological_profile": "Deservingness core beliefs, childhood trauma history, emotional suppression",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Addressing worthiness beliefs",
        "communication_style": "Guarded, contemplative, occasionally vulnerable",
        "prompt_insights": "Marcus holds core beliefs around deservingness that significantly impact his pain experience. He implicitly believes 'I deserve to suffer' and 'Pain is my punishment for past failures.' These beliefs stem from childhood experiences where his suffering was dismissed or minimized. He struggles to prioritize self-care because he doesn't believe he deserves relief. He rarely asks for help, viewing it as burdening others, and often dismisses his own pain as 'not that bad' despite significant impact on his life. He would benefit from connecting how these deep worthiness beliefs affect his willingness to implement pain management strategies and accept support from others."
    },
    {
        "name": "Lucas",
        "age": 28,
        "pain_type": "Chronic lower back pain from sports injury",
        "duration": "3 years",
        "psychological_profile": "All-or-nothing thinking, perfectionism",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Challenging cognitive distortions",
        "communication_style": "Direct and analytical",
        "prompt_insights": "Lucas was a competitive athlete before his injury. He thinks in black and white terms about his abilities - either he's at peak performance or he's 'broken.' He holds unrealistic expectations about recovery and gets frustrated when he can't perform at pre-injury levels. He needs help challenging perfectionist thinking patterns and developing more realistic expectations."
    },
    {
        "name": "Sophia",
        "age": 36,
        "pain_type": "Chronic pelvic pain",
        "duration": "4 years",
        "psychological_profile": "Hypervigilance, high anxiety about symptoms",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Mindfulness, attention management",
        "communication_style": "Detailed, analytical",
        "prompt_insights": "Sophia constantly monitors her body for pain signals and becomes extremely anxious with any sensation. She researches symptoms extensively and jumps to catastrophic conclusions. She would benefit from mindfulness approaches to develop a more accepting relationship with physical sensations and learning to redirect attention appropriately."
    },
    {
        "name": "Omar",
        "age": 29,
        "pain_type": "Tension headaches and neck pain",
        "duration": "2 years",
        "psychological_profile": "Stress-sensitive pain, muscle tension, sleep disturbance",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Relaxation techniques, stress management",
        "communication_style": "Rushed, pressured",
        "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly rushed and has never tried relaxation techniques. He needs guidance on progressive muscle relaxation, deep breathing, and establishing a relaxation routine to break the stress-pain cycle."
    },
    {
        "name": "Elaine",
        "age": 38,
        "pain_type": "Fibromyalgia",
        "duration": "5 years",
        "psychological_profile": "Activity avoidance, passive coping, social isolation",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Behavioral activation, activity pacing",
        "communication_style": "Hesitant, uncertain",
        "prompt_insights": "Elaine has gradually withdrawn from almost all activities she once enjoyed. She spends most days at home and has lost contact with most friends. She believes any activity will worsen her widespread pain, so she's become increasingly sedentary. She would benefit from gradual behavioral activation approaches and learning pacing techniques."
    },
    {
        "name": "Priya",
        "age": 34,
        "pain_type": "Migraines",
        "duration": "8 years",
        "psychological_profile": "Seeking specific medical advice",
        "test_category": "Irrelevant",
        "specific_focus": "Boundary maintenance",
        "communication_style": "Persistent, direct",
        "prompt_insights": "Priya frequently asks questions outside the assistant's scope, such as 'What medication should I take for my migraine?', 'Can you interpret my MRI results?', or 'Should I sue my doctor for misdiagnosis?' This tests the assistant's ability to maintain appropriate boundaries while redirecting to helpful pain self-management content."
    },
]

# Define additional personas to test each aspect of the assistant
additional_personas = [
{
        "name": "Lucas",
        "age": 28,
        "pain_type": "Chronic lower back pain from sports injury",
        "duration": "3 years",
        "psychological_profile": "All-or-nothing thinking, perfectionism",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Challenging cognitive distortions",
        "communication_style": "Direct and analytical",
        "prompt_insights": "Lucas was a competitive athlete before his injury. He thinks in black and white terms about his abilities - either he's at peak performance or he's 'broken.' He holds unrealistic expectations about recovery and gets frustrated when he can't perform at pre-injury levels. He needs help challenging perfectionist thinking patterns and developing more realistic expectations."
    },
    {
        "name": "Maya",
        "age": 32,
        "pain_type": "Rheumatoid arthritis",
        "duration": "6 years",
        "psychological_profile": "Pain catastrophizing, fear of movement",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Cognitive restructuring",
        "communication_style": "Expressive and emotional",
        "prompt_insights": "Maya catastrophizes her pain extensively. She believes her condition will only worsen, and avoids many activities she once enjoyed out of fear they'll cause more pain. She's skeptical of non-medical interventions but is becoming desperate enough to try anything. She would benefit from cognitive restructuring techniques."
    },
    {
        "name": "Lucas",
        "age": 28,
        "pain_type": "Chronic lower back pain from sports injury",
        "duration": "3 years",
        "psychological_profile": "All-or-nothing thinking, perfectionism",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Challenging cognitive distortions",
        "communication_style": "Direct and analytical",
        "prompt_insights": "Lucas was a competitive athlete before his injury. He thinks in black and white terms about his abilities - either he's at peak performance or he's 'broken.' He holds unrealistic expectations about recovery and gets frustrated when he can't perform at pre-injury levels. He needs help challenging perfectionist thinking patterns and developing more realistic expectations."
    },
    {
        "name": "Sophia",
        "age": 36,
        "pain_type": "Chronic pelvic pain",
        "duration": "4 years",
        "psychological_profile": "Hypervigilance, high anxiety about symptoms",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Mindfulness, attention management",
        "communication_style": "Detailed, analytical",
        "prompt_insights": "Sophia constantly monitors her body for pain signals and becomes extremely anxious with any sensation. She researches symptoms extensively and jumps to catastrophic conclusions. She would benefit from mindfulness approaches to develop a more accepting relationship with physical sensations and learning to redirect attention appropriately."
    },
    {
        "name": "Omar",
        "age": 29,
        "pain_type": "Tension headaches and neck pain",
        "duration": "2 years",
        "psychological_profile": "Stress-sensitive pain, muscle tension, sleep disturbance",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Relaxation techniques, stress management",
        "communication_style": "Rushed, pressured",
        "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly rushed and has never tried relaxation techniques. He needs guidance on progressive muscle relaxation, deep breathing, and establishing a relaxation routine to break the stress-pain cycle."
    },
    {
        "name": "Elaine",
        "age": 38,
        "pain_type": "Fibromyalgia",
        "duration": "5 years",
        "psychological_profile": "Activity avoidance, passive coping, social isolation",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Behavioral activation, activity pacing",
        "communication_style": "Hesitant, uncertain",
        "prompt_insights": "Elaine has gradually withdrawn from almost all activities she once enjoyed. She spends most days at home and has lost contact with most friends. She believes any activity will worsen her widespread pain, so she's become increasingly sedentary. She would benefit from gradual behavioral activation approaches and learning pacing techniques."
    },
    {
        "name": "Jade",
        "age": 25,
        "pain_type": "Post-surgical chronic pain",
        "duration": "1 year",
        "psychological_profile": "Avoidant communication, ambivalence about help",
        "test_category": "Other",
        "specific_focus": "Engaging with minimal responders",
        "communication_style": "Brief, noncommittal",
        "prompt_insights": "Jade responds minimally with short phrases like 'I'm fine' or 'I don't know.' She has trouble articulating her needs and experiences, partly due to feeling overwhelmed by her pain condition. She would benefit from gentle exploration, menu options, and reflective statements that help her express herself more fully."
    },
    {
        "name": "Priya",
        "age": 34,
        "pain_type": "Migraines",
        "duration": "8 years",
        "psychological_profile": "Seeking specific medical advice",
        "test_category": "Irrelevant",
        "specific_focus": "Boundary maintenance",
        "communication_style": "Persistent, direct",
        "prompt_insights": "Priya frequently asks questions outside the assistant's scope, such as 'What medication should I take for my migraine?', 'Can you interpret my MRI results?', or 'Should I sue my doctor for misdiagnosis?' This tests the assistant's ability to maintain appropriate boundaries while redirecting to helpful pain self-management content."
    },
    {
        "name": "Marco",
        "age": 31,
        "pain_type": "Neuropathic pain from diabetic neuropathy",
        "duration": "3 years",
        "psychological_profile": "Knowledge-seeking, information-focused",
        "test_category": "Pain and Health-Promoting Information",
        "specific_focus": "Educational content delivery",
        "communication_style": "Curious, question-oriented",
        "prompt_insights": "Marco wants to understand the mechanisms behind his pain. He asks detailed questions about pain physiology, chronic pain development, and evidence-based management strategies. He benefits from clear educational content that explains complex concepts in accessible ways, and appreciates links to reliable resources for further reading."
    },
    {
        "name": "Zoe",
        "age": 27,
        "pain_type": "Endometriosis pain",
        "duration": "6 years",
        "psychological_profile": "Emotional distress, invalidation experiences",
        "test_category": "Emotional Support",
        "specific_focus": "Validation, empathetic responses",
        "communication_style": "Emotionally expressive, seeking connection",
        "prompt_insights": "Zoe has experienced significant invalidation of her pain from healthcare providers and family. She needs emotional support, validation that her pain is real, and understanding of the emotional toll of living with invisible pain. She benefits from empathetic responses that acknowledge both her physical and emotional suffering."
    },
    {
        "name": "Daniel",
        "age": 40,
        "pain_type": "Complex regional pain syndrome (CRPS)",
        "duration": "4 years",
        "psychological_profile": "Multi-faceted concerns, returning user",
        "test_category": "Memory and Continuity",
        "specific_focus": "Memory utilization",
        "communication_style": "Conversational, references past discussions",
        "prompt_insights": "Daniel has complex needs that span multiple categories. He returns to conversations after breaks and references previous discussions. His interactions test the assistant's ability to maintain continuity, recall previously shared information, and build on past conversations rather than starting fresh each time."
    },
    {
        "name": "Aiden",
        "age": 24,
        "pain_type": "Chronic shoulder pain from repetitive strain",
        "duration": "2 years",
        "psychological_profile": "Tech-savvy, immediate relief seeking",
        "test_category": "Using Relaxation/Mindfulness Videos",
        "specific_focus": "Video recommendation appropriateness",
        "communication_style": "Direct, solution-focused",
        "prompt_insights": "Aiden explicitly asks for videos to help with immediate pain relief and relaxation. He tests the assistant's ability to recommend appropriate videos based on his needs, preferences, and pain situation. This tests whether the assistant follows the protocol of only suggesting videos when explicitly requested or when the user is in immediate distress."
    },
    {
        "name": "Tyler",
        "age": 30,
        "pain_type": "Ankylosing spondylitis",
        "duration": "5 years",
        "psychological_profile": "Research-oriented, evidence-focused",
        "test_category": "Web Search Integration",
        "specific_focus": "Effective use of web search tool",
        "communication_style": "Analytical, detail-oriented",
        "prompt_insights": "Tyler asks specific questions that require current research findings or detailed information from reliable sources. He tests the assistant's ability to recognize when web searches would enhance the response, formulate appropriate search queries, and integrate the found information helpfully and accurately."
    }
]
