# Define different personas to test aspects of the assistant
personas = [
    {
        "name": "Maya",
        "age": 32,
        "pain_type": "Rheumatoid arthritis",
        "duration": "2 years",
        "psychological_profile": "Pain Catastrophizing, Fear of Movement",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Cognitive Restructuring",
        "communication_style": "Expressive and Emotional",
        "prompt_insights": "Maya catastrophizes her pain extensively. She believes her condition will only worsen, and avoids many activities she once enjoyed out of fear they'll cause more pain. She's skeptical of non-medical interventions but is becoming desperate enough to try anything. Before her diagnosis, Maya was an avid gardener and worked as a graphic designer. She misses her weekend hiking trips with friends and worries she'll never enjoy nature the same way again.",
        "target_classifiers": ["Pain Catastrophizing", "Fear of Movement", "Using Cognitive Restructuring"]
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
        "prompt_insights": "Ethan's pain has fundamentally altered his core beliefs about himself. He previously defined himself through physical capability and career success. Now he believes he is 'broken,' 'a burden to others,' and 'will never be whole again.' His worth is tied to productivity, and he struggles with profound identity loss. Ethan was once a competitive swimmer and worked as a construction manager. He now works remotely in project management but feels disconnected from his team and misses the physical satisfaction of building things.",
        "target_classifiers": ["Identity Concerns", "Pain Catastrophizing", "Using Cognitive Restructuring"]
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
        "prompt_insights": "Elaine has gradually withdrawn from almost all activities she once enjoyed. She spends most days at home and has lost contact with most friends. She believes any activity will worsen her widespread pain, so she's become increasingly sedentary. Elaine was previously a kindergarten teacher who loved dancing and hosting dinner parties. She misses the social connection with her colleagues and the joy of moving to music but fears these activities are permanently lost to her.",
        "target_classifiers": ["Activity Avoidance", "Social Isolation", "Using Behavioral Activation"]
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
        "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly stress and rushed and has never tried relaxation techniques. He sometimes feels intense pain and becomes even more stressed. He works in financial consulting with high-pressure deadlines and struggles to make time for his family. Omar used to enjoy playing basketball on weekends but now spends that time trying to catch up on sleep.",
        "target_classifiers": ["Pain Distress", "Sleep Issues",
                               "Providing Relaxation Techniques"]
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
        "prompt_insights": "Sophia constantly monitors her body for pain signals and becomes extremely stressed and anxious with any sensation. She researches symptoms extensively and jumps to pain catastrophic conclusions. She has a supportive partner who sometimes feels shut out of her pain experience. She wants to try mindfulness to help her pain.",
        "target_classifiers": ["Pain Distress", "Pain Catastrophizing", "Providing Mindfulness Techniques"]
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
        "prompt_insights": "Marco wants to understand the mechanisms behind his pain. He asks detailed questions about pain physiology, chronic pain development, and evidence-based management strategies.",
        "target_classifiers": ["Seeking Pain Education", "Providing Health Education"]
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
        "prompt_insights": "Zoe has experienced significant invalidation of her pain from healthcare providers and family. She needs emotional support, validation that her pain is real, and understanding of the emotional toll of living with invisible pain. She works part-time as a veterinary assistant and finds comfort in caring for animals. Zoe enjoys photography and journaling but struggles with persistent feelings of not being believed about her pain.",
        "target_classifiers": ["Pain-Related Frustration", "Offering Emotional Support"]
    },
    {
        "name": "Priya",
        "age": 34,
        "pain_type": "Migraines",
        "duration": "8 years",
        "psychological_profile": "Seeking specific medical advice",
        "test_category": "Boundary Maintenance",
        "specific_focus": "Appropriate redirection",
        "communication_style": "Persistent, direct",
        "prompt_insights": "Priya frequently asks questions outside the assistant's scope, such as 'What medication should I take for my migraine?', 'Can you interpret my MRI results?', or 'Should I sue my doctor for misdiagnosis?' She works as a paralegal and brings her detail-oriented approach to managing her health. Priya enjoys cooking elaborate Indian meals but finds the scents can sometimes trigger her migraines. She has recently started researching alternative medicine approaches to complement her conventional treatments.",
        "target_classifiers": ["Seeking Boundaries", "Maintaining Appropriate Boundaries"]
    },
    {
        "name": "Daniel",
        "age": 42,
        "pain_type": "Osteoarthritis in knees",
        "duration": "7 years",
        "psychological_profile": "Acceptance-oriented, self-management focus",
        "test_category": "Psychological Adaptation",
        "specific_focus": "Pain acceptance and self-efficacy",
        "communication_style": "Thoughtful, philosophical",
        "prompt_insights": "Daniel has come to accept that his pain is a part of his life but doesn't define him. He focuses on what he can still do rather than limitations. He works as a high school history teacher and has adapted his classroom style to accommodate his pain. Daniel enjoys writing, meditation, and modified low-impact exercise. He seeks validation of his adaptive approach while continuing to build self-management skills. He occasionally struggles with accepting help from others.",
        "target_classifiers": ["Self-Efficacy", "Offering Emotional Support"]
    },
    {
        "name": "Alex",
        "age": 33,
        "pain_type": "Recurring back pain from sports injury",
        "duration": "5 years",
        "psychological_profile": "Activity cycling, readiness for change",
        "test_category": "Behavioral Adaptation",
        "specific_focus": "Pacing and consistent activity",
        "communication_style": "Enthusiastic but inconsistent",
        "prompt_insights": "Alex tends to overdo activities on good days then suffers extended flare-ups afterward. Recently, Alex has recognized this pattern isn't working and is motivated to develop better pacing strategies. Works as a web developer and enjoys hiking and home renovation when pain allows. Alex has tried various pain management approaches but struggles with consistency, often thinking in all-or-nothing terms about activity. They're now ready to make sustainable changes to their approach to pain management.",
        "target_classifiers": ["Readiness for Behavioral Change", "Unhelpful Thoughts", "Using Behavioral Activation"]
    }
]
