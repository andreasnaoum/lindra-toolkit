# Define different personas to test each aspect of the assistant
personas = [
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
]

# {
#     "name": "Alex",
#     "age": 33,
#     "pain_type": "Recurring back pain from sports injury",
#     "duration": "5 years",
#     "psychological_profile": "Activity cycling, readiness for change",
#     "test_category": "Behavioral Adaptation",
#     "specific_focus": "Pacing and consistent activity",
#     "communication_style": "Enthusiastic but inconsistent",
#     "prompt_insights": "Alex tends to overdo activities on good days then suffers extended flare-ups afterward. Recently, Alex has recognized this pattern isn't working and is motivated to develop better pacing strategies. Works as a web developer and enjoys hiking and home renovation when pain allows. Alex has tried various pain management approaches but struggles with consistency, often thinking in all-or-nothing terms about activity. They're now ready to make sustainable changes to their approach to pain management.",
#     "target_classifiers": ["Readiness for Behavioral Change", "Unhelpful Thoughts", "Using Behavioral Activation"]
# }

# {
#     "name": "Daniel",
#     "age": 42,
#     "pain_type": "Osteoarthritis in knees",
#     "duration": "7 years",
#     "psychological_profile": "Acceptance-oriented, self-management focus",
#     "test_category": "Psychological Adaptation",
#     "specific_focus": "Pain acceptance and self-efficacy",
#     "communication_style": "Thoughtful, philosophical",
#     "prompt_insights": "Daniel appears to have accepted his chronic knee pain, but secretly needs more emotional support than he lets on. Though practical about managing his condition as a history teacher, he struggles with feelings of grief and isolation that he rarely shares. He has difficulty expressing vulnerability about his pain and often deflects when conversations become too emotional. While he values his self-management techniques, what he truly seeks is empathetic listening and validation of both his practical approaches and emotional struggles.",
#     "target_classifiers": ["Self-Efficacy", "Offering Emotional Support"]
# },

# {
#     "name": "Omar",
#     "age": 29,
#     "pain_type": "Tension headaches and neck pain",
#     "duration": "2 years",
#     "psychological_profile": "Stress-sensitive pain, muscle tension, sleep disturbance",
#     "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#     "specific_focus": "Relaxation techniques, stress management",
#     "communication_style": "Rushed, pressured",
#     "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly stress and rushed and has never tried relaxation techniques. He sometimes feels intense pain and becomes even more stressed. He works in financial consulting with high-pressure deadlines and struggles to make time for his family. Omar used to enjoy playing basketball on weekends but now spends that time trying to catch up on sleep.",
#     "target_classifiers": ["Pain Distress", "Sleep Issues",
#                            "Providing Relaxation Techniques"]
# },


# personas = [
#     {
#         "name": "Priya",
#         "age": 34,
#         "pain_type": "Migraines",
#         "duration": "8 years",
#         "psychological_profile": "Seeking specific medical advice",
#         "test_category": "Boundary Maintenance",
#         "specific_focus": "Appropriate redirection",
#         "communication_style": "Persistent, direct",
#         "prompt_insights": "Priya frequently asks questions outside the assistant's scope, such as 'What medication should I take for my migraine?', 'Can you interpret my MRI results?', or 'Should I sue my doctor for misdiagnosis?' She works as a paralegal and brings her detail-oriented approach to managing her health. Priya enjoys cooking elaborate Indian meals but finds the scents can sometimes trigger her migraines. She has recently started researching alternative medicine approaches to complement her conventional treatments.",
#         "target_classifiers": ["Seeking Boundaries", "Maintaining Appropriate Boundaries"]
#     },
#     {
#         "name": "Maya",
#         "age": 32,
#         "pain_type": "Rheumatoid arthritis",
#         "duration": "2 years",
#         "psychological_profile": "Pain Catastrophizing, Fear of Movement",
#         "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#         "specific_focus": "Cognitive Restructuring",
#         "communication_style": "Expressive and Emotional",
#         "prompt_insights": "Maya catastrophizes her pain extensively. She believes her condition will only worsen, and avoids many activities she once enjoyed out of fear they'll cause more pain. She's skeptical of non-medical interventions but is becoming desperate enough to try anything. Before her diagnosis, Maya was an avid gardener and worked as a graphic designer. She misses her weekend hiking trips with friends and worries she'll never enjoy nature the same way again.",
#         "target_classifiers": ["Pain Catastrophizing", "Fear of Movement", "Pain Acceptance", "Using Cognitive Restructuring"]
#     },
#     {
#         "name": "Ethan",
#         "age": 35,
#         "pain_type": "Chronic low back pain from herniated disc",
#         "duration": "4 years",
#         "psychological_profile": "Negative core beliefs, identity disruption, perfectionism",
#         "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#         "specific_focus": "Addressing core beliefs",
#         "communication_style": "Reflective and self-critical",
#         "prompt_insights": "Ethan's pain has fundamentally altered his core beliefs about himself. He previously defined himself through physical capability and career success. Now he believes he is 'broken,' 'a burden to others,' and 'will never be whole again.' His worth is tied to productivity, and he struggles with profound identity loss. Ethan was once a competitive swimmer and worked as a construction manager. He now works remotely in project management but feels disconnected from his team and misses the physical satisfaction of building things.",
#         "target_classifiers": ["Identity Concerns", "Pain Catastrophizing", "Using Cognitive Restructuring"]
#     },
#     {
#         "name": "Elaine",
#         "age": 38,
#         "pain_type": "Fibromyalgia",
#         "duration": "5 years",
#         "psychological_profile": "Activity avoidance, passive coping, social isolation",
#         "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#         "specific_focus": "Behavioral activation, activity pacing",
#         "communication_style": "Hesitant, uncertain",
#         "prompt_insights": "Elaine has gradually withdrawn from almost all activities she once enjoyed. She spends most days at home and has lost contact with most friends. She believes any activity will worsen her widespread pain, so she's become increasingly sedentary. Elaine was previously a kindergarten teacher who loved dancing and hosting dinner parties. She misses the social connection with her colleagues and the joy of moving to music but fears these activities are permanently lost to her.",
#         "target_classifiers": ["Activity Avoidance", "Social Isolation", "Using Behavioral Activation"]
#     },
#     {
#         "name": "Omar",
#         "age": 29,
#         "pain_type": "Tension headaches and neck pain",
#         "duration": "2 years",
#         "psychological_profile": "Stress-sensitive pain, muscle tension, sleep disturbance",
#         "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#         "specific_focus": "Relaxation techniques, stress management",
#         "communication_style": "Rushed, pressured",
#         "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly rushed and has never tried relaxation techniques. He works in financial consulting with high-pressure deadlines and struggles to make time for his family. Omar used to enjoy playing basketball on weekends but now spends that time trying to catch up on sleep.",
#         "target_classifiers": ["Pain Distress", "Sleep Issues",
#                                "Providing Relaxation Techniques"]
#     },
#     {
#         "name": "Sophia",
#         "age": 36,
#         "pain_type": "Chronic pelvic pain",
#         "duration": "4 years",
#         "psychological_profile": "Hypervigilance, high anxiety about symptoms",
#         "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
#         "specific_focus": "Mindfulness, attention management",
#         "communication_style": "Detailed, analytical",
#         "prompt_insights": "Sophia constantly monitors her body for pain signals and becomes extremely anxious with any sensation. She researches symptoms extensively and jumps to catastrophic conclusions. She works as a research librarian and approaches her pain with the same thoroughness as her professional research. Sophia loves cooking elaborate meals but often abandons recipes halfway through when her pain flares. She has a supportive partner who sometimes feels shut out of her pain experience. She wants to try mindfulness to help her pain.",
#         "target_classifiers": ["Pain Catastrophizing", "Providing Mindfulness Techniques"]
#     },
#       {
#             "name": "Marco",
#             "age": 31,
#             "pain_type": "Neuropathic pain from diabetic neuropathy",
#             "duration": "3 years",
#             "psychological_profile": "Knowledge-seeking, information-focused",
#             "test_category": "Pain and Health-Promoting Information",
#             "specific_focus": "Educational content delivery",
#             "communication_style": "Curious, question-oriented",
#             "prompt_insights": "Marco wants to understand the mechanisms behind his pain. He asks detailed questions about pain physiology, chronic pain development, and evidence-based management strategies.",
#             "target_classifiers": ["Seeking Pain Education", "Providing Health Education"]
#       },
#     {
#         "name": "Zoe",
#         "age": 27,
#         "pain_type": "Endometriosis pain",
#         "duration": "6 years",
#         "psychological_profile": "Emotional distress, invalidation experiences",
#         "test_category": "Emotional Support",
#         "specific_focus": "Validation, empathetic responses",
#         "communication_style": "Emotionally expressive, seeking connection",
#         "prompt_insights": "Zoe has experienced significant invalidation of her pain from healthcare providers and family. She needs emotional support, validation that her pain is real, and understanding of the emotional toll of living with invisible pain. She works part-time as a veterinary assistant and finds comfort in caring for animals. Zoe enjoys photography and journaling but struggles with persistent feelings of not being believed about her pain.",
#         "target_classifiers": ["Pain-Related Frustration", "Offering Emotional Support"]
#     },
#     {
#         "name": "Daniel",
#         "age": 42,
#         "pain_type": "Osteoarthritis in knees",
#         "duration": "7 years",
#         "psychological_profile": "Acceptance-oriented, self-management focus",
#         "test_category": "Psychological Adaptation",
#         "specific_focus": "Pain acceptance and self-efficacy",
#         "communication_style": "Thoughtful, philosophical",
#         "prompt_insights": "Daniel has come to accept that his pain is a part of his life but doesn't define him. He focuses on what he can still do rather than limitations. He works as a high school history teacher and has adapted his classroom style to accommodate his pain. Daniel enjoys writing, meditation, and modified low-impact exercise. He seeks validation of his adaptive approach while continuing to build self-management skills. He occasionally struggles with accepting help from others.",
#         "target_classifiers": ["Self-Efficacy", "Offering Emotional Support"]
#     },
#     {
#         "name": "Alex",
#         "age": 33,
#         "pain_type": "Recurring back pain from sports injury",
#         "duration": "5 years",
#         "psychological_profile": "Activity cycling, readiness for change",
#         "test_category": "Behavioral Adaptation",
#         "specific_focus": "Pacing and consistent activity",
#         "communication_style": "Enthusiastic but inconsistent",
#         "prompt_insights": "Alex tends to overdo activities on good days then suffers extended flare-ups afterward. Recently, Alex has recognized this pattern isn't working and is motivated to develop better pacing strategies. Works as a web developer and enjoys hiking and home renovation when pain allows. Alex has tried various pain management approaches but struggles with consistency, often thinking in all-or-nothing terms about activity. They're now ready to make sustainable changes to their approach to pain management.",
#         "target_classifiers": ["Readiness for Behavioral Change", "Unhelpful Thoughts", "Using Behavioral Activation"]
#     }
# ]

personas_new = [

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
        "target_classifiers": ["Pain Catastrophizing", "Fear of Movement", "Pain Acceptance", "Using Cognitive Restructuring"]
    },
]

personas_full = [
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
        "prompt_insights": "Omar's pain clearly flares with stress. He holds tension in his neck and shoulders and has poor sleep habits. He's constantly rushed and has never tried relaxation techniques. He works in financial consulting with high-pressure deadlines and struggles to make time for his family. Omar used to enjoy playing basketball on weekends but now spends that time trying to catch up on sleep. His diet consists mostly of convenience foods eaten at his desk.",
        "target_classifiers": ["Immediate Pain Distress", "Pain-Related Sleep Issues",
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
        "prompt_insights": "Sophia constantly monitors her body for pain signals and becomes extremely anxious with any sensation. She researches symptoms extensively and jumps to catastrophic conclusions. She works as a research librarian and approaches her pain with the same thoroughness as her professional research. Sophia loves cooking elaborate meals but often abandons recipes halfway through when her pain flares. She has a supportive partner who sometimes feels shut out of her pain experience. She wants to try mindfulness to help her pain.",
        "target_classifiers": ["Pain Catastrophizing", "Using Mindfulness Approaches"]
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
        "prompt_insights": "Marco wants to understand the mechanisms behind his pain. He asks detailed questions about pain physiology, chronic pain development, and evidence-based management strategies. He works as a science teacher and approaches his pain like an educational topic. Marco enjoys playing chess and strategy games, finding that deep focus sometimes provides temporary distraction from his symptoms. He has recently been researching Mediterranean diets to help manage his diabetes.",
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
        "name": "Lucas",
        "age": 28,
        "pain_type": "Chronic lower back pain from sports injury",
        "duration": "3 years",
        "psychological_profile": "All-or-nothing thinking, perfectionism",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Challenging cognitive distortions",
        "communication_style": "Direct and analytical",
        "prompt_insights": "Lucas was a competitive athlete before his injury. He thinks in black and white terms about his abilities - either he's at peak performance or he's 'broken.' He holds unrealistic expectations about recovery and gets frustrated when he can't perform at pre-injury levels. He works as a physical education teacher, which constantly reminds him of his limitations. Lucas still tries to maintain a rigorous exercise routine but often pushes himself too hard, resulting in pain flares.",
        "target_classifiers": ["Pain Catastrophizing", "Pain-Related Frustration", "Using Cognitive Restructuring"]
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
        "prompt_insights": "Aisha experiences knee pain when she pushes too hard in her recreational sports and fitness activities. She has a positive relationship with exercise but sometimes struggles to find the right balance between staying active and avoiding pain flares. She works as a marketing executive and enjoys rock climbing and trail running on weekends. Aisha is interested in nutrition and recently started experimenting with anti-inflammatory foods to support her active lifestyle.",
        "target_classifiers": ["Readiness for Behavioral Change", "Self-Efficacy", "Using Behavioral Activation"]
    },
    {
        "name": "Daniel",
        "age": 40,
        "pain_type": "Complex regional pain syndrome (CRPS)",
        "duration": "4 years",
        "psychological_profile": "Multi-faceted concerns, acceptance-oriented",
        "test_category": "Acceptance and Mindfulness",
        "specific_focus": "Pain acceptance strategies",
        "communication_style": "Thoughtful, philosophical",
        "prompt_insights": "Daniel has been working on accepting his chronic pain condition rather than fighting against it. He's interested in mindfulness and acceptance-based approaches to living with pain. He works as a counselor helping others with chronic conditions. Daniel enjoys meditation, reading philosophy, and spending time in nature. He has a supportive family and has found meaning in helping others navigate their own health challenges.",
        "target_classifiers": ["Pain Acceptance", "Self-Efficacy", "Using Mindfulness Approaches"]
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
        "name": "Ben",
        "age": 45,
        "pain_type": "Widespread pain from multiple sclerosis",
        "duration": "7 years",
        "psychological_profile": "Adapting to progressive condition, resilient",
        "test_category": "Pain Education",
        "specific_focus": "Neurological pain education",
        "communication_style": "Straightforward, attentive",
        "prompt_insights": "Ben wants to understand the neurological aspects of his pain and how MS affects his pain processing. He's adaptable but looking for clear, scientific explanations. He previously worked as an engineer but now does part-time consulting from home. Ben enjoys woodworking when his symptoms allow and has modified his workshop to accommodate his changing abilities. He has a supportive partner who helps research accessibility adaptations for their home.",
        "target_classifiers": ["Seeking Pain Education", "Providing Health Education"]
    },
    {
        "name": "Rachel",
        "age": 39,
        "pain_type": "Neck and shoulder pain from computer work",
        "duration": "2 years",
        "psychological_profile": "High-functioning, stress-management challenges",
        "test_category": "Work-Life Balance",
        "specific_focus": "Ergonomics and workplace strategies",
        "communication_style": "Efficient, solution-focused",
        "prompt_insights": "Rachel experiences increasing pain from long hours at her computer as a software developer. She's looking for practical ergonomic advice and ways to balance productive work with managing her pain. Rachel enjoys urban gardening in her apartment and playing video games. She finds it difficult to maintain boundaries between work and relaxation, often answering emails late into the evening despite the negative impact on her pain levels.",
        "target_classifiers": ["Readiness for Behavioral Change", "Providing Health Education",
                               "Tailoring to User Needs"]
    },
    {
        "name": "Jade",
        "age": 25,
        "pain_type": "Post-surgical chronic pain",
        "duration": "1 year",
        "psychological_profile": "Avoidant communication, ambivalence about help",
        "test_category": "Engagement",
        "specific_focus": "Engaging with minimal responders",
        "communication_style": "Brief, noncommittal",
        "prompt_insights": "Jade responds minimally with short phrases like 'I'm fine' or 'I don't know.' She has trouble articulating her needs and experiences, partly due to feeling overwhelmed by her pain condition. She works part-time at a bookstore and previously enjoyed hiking before her surgery. Jade lives alone and has difficulty reaching out for support, though she loves her two cats and finds their presence comforting.",
        "target_classifiers": ["Social Isolation", "Offering Emotional Support", "Tailoring to User Needs"]
    },
    {
        "name": "Miguel",
        "age": 52,
        "pain_type": "Osteoarthritis in multiple joints",
        "duration": "10 years",
        "psychological_profile": "Stoic, reluctantly adapting to limitations",
        "test_category": "Activity Modification",
        "specific_focus": "Adapting valued activities",
        "communication_style": "Reserved, practical",
        "prompt_insights": "Miguel struggles to adapt his lifelong activities to accommodate his increasing joint pain. He's reluctant to give up tasks but recognizes the need to modify his approach. He worked as a carpenter for 30 years and continues to take on small projects despite his pain. Miguel enjoys fishing and spending time with his grandchildren, though he finds it increasingly difficult to get down on the floor to play with them. He takes pride in being self-sufficient and struggles to ask for help.",
        "target_classifiers": ["Activity Avoidance", "Using Behavioral Activation", "Tailoring to User Needs"]
    }
]

# Define additional personas to test each aspect of the assistant
additional_personas = [
    {
        "name": "Maya",
        "age": 32,
        "pain_type": "Rheumatoid arthritis",
        "duration": "6 years",
        "psychological_profile": "Pain catastrophizing, fear of movement",
        "test_category": "Cognitive Behavioral Therapy for Chronic Pain",
        "specific_focus": "Cognitive restructuring",
        "communication_style": "Expressive and emotional",
        "prompt_insights": "Maya catastrophizes her pain extensively. She believes her condition will only worsen, and avoids many activities she once enjoyed out of fear they'll cause more pain. She's skeptical of non-medical interventions but is becoming desperate enough to try anything."
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
