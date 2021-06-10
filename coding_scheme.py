##% This file defines the full MHINT coding scheme for use in the main data processing files.

# Import packages
import pandas as pd

# Define all behavioural groups/codes and behaviours/subcodes
view                       = ["Full View", "Partial View", "No View"]
audio                      = ["Audible", "Partially Audible", "No audio"]
alertness_state            = ["Drowsy/semi-dozing state", "Asleep state", "Alert/wakeful state", "Crying state", "Not possible to code alertness state"]
caregiver_proximity        = ["Out of reach", "Within reach", "Loom", "Not possible to code caregiver proximity"]
caregiver_body_orientation = ["Body oriented to infant", "Body oriented to other caregiver", "Body oriented to sibling (c)", "Body oriented to other person/object", 
                              "Body oriented to object (focus of the activity)", "Not possible to code caregiver body orientation"]
infant_body_orientation    = ["Body oriented to caregiver 1", "Body oriented to caregiver 2", "Body oriented to sibling", "Body oriented to different person/object", 
                              "Body oriented to object (focus of activity)", "Not possible to code infant body orientation"]
head_orientation           = ["Vis-a-vis - infant and caregiver", "Slight (30-90 degree) aversion right", "Slight (30-90 degree) aversion left", "Full (90 degree) aversion right", 
                              "Full (90 degree) aversion left", "Arch aversion", "Head not in view of infant", "Not possible to code head orientation"]
visual_attention           = ["Look at infant", "Look at caregiver 1", "Look at caregiver 2", "Look at same object/joint attention", "Look at focus object", 
                              "Look at different object", "Look at other object", "Look at object outside of view", "Look at sibling", "Look at other person", 
                              "Look at distraction", "No visual attention", "Not possible to code visual attention"]
facial_expression          = ["Neutral/Alert", "Positive", "Smile", "Negative", "Disgust", "Surprise", "Woe face", "Mock surprise", "Face not visible", "None of the above"]
caregiver_posture          = ["Lying down", "Lie on side", "Sit on floor", "Sit on object", "Stand up", "Crawl", "Crouched down", "Jump", "Walk", "Run", "Dance", 
                              "Not possible to code caregiver posture/action"]
infant_posture             = ["Lie down", "Lie on one side", "Sit on the floor", "Sit on an object", "Standing", "Crawling", "Jumping", "Walking", "Running", "Held/in hold", 
                              "Try to move in another way", "Not possible to code infant posture/action"]
touch_right_hand           = ["Infant touch R", "Caregiver touch R", "No infant touch R", "No caregiver touch R", "Not possible to code touch R"]
touch_left_hand            = ["Infant touch L", "Caregiver touch L", "No infant touch L", "No caregiver touch L", "Not possible to code touch L"]
hand_movements             = ["Pointing", "Reaching", "Clapping", "Waving", "Gesticulating", "Banging", "Other hand movements", "No hand movements", "Not possible to code hand movements"]
encouragement              = ["Caregiver encouragement to focus object", "Caregiver encouragement to other object/person", "Caregiver encouragement of infant motor skills", 
                              "Caregiver discouragement from focus object", "Caregiver discouragement from caregiver", "Caregiver discouragement from other person/object", 
                              "Caregiver discouragement of infant motor skills", "No encouragement/discouragement", "Not possible to code encouragement/discouragement"]
agitation_soothing         = ["Agitation", "Self-soothing", "No agitation/soothing", "Not possible to code agitation/soothing"]
acknowledgment             = ["Yes, non-verbal acknowledgment", "No non-verbal acknowledgment", "Not possible to code"]
physical_imitation         = ["Physical imitation evident", "No physical imitation", "Not possible to code physical imitation"]
physical_play              = ["Physical play evident", "No physical play", "Not possible to code physical play"]
rough_and_tumble           = ["Suspense/surprise", "Manipulation of infant's part of the body", "No rough and Tumble Play", "Not possible to code rough and tumble play"]
caregiver_vocalisation     = ["Speech", "Musical Sounds", "Laugh", "Nervous laugh", "Vocal Imitation", "Bodily sounds", "Scream", "Vocal tics", "Non verbal sound", 
                              "Silent", "Not possible to code caregiver vocalisation"]
infant_vocalisation        = ["Laughing", "Distressed", "Non-Distress", "Imitating sounds", "Babbling", "First words", "Screaming", "Bodily Sounds", "Silent/none of the above", 
                              "Not possible to code infant vocalisation"]
caregiver_unusual_behaviours = ["Exaggerated emotional response", "Hoarding", "Washing (compulsively)", "Checking (with no functionality)", 
                                "Counting (with no functionality)", "Arranging and ordering objects (with no functionality)", "Physical tics", "Bared teeth", 
                                "Submissive behaviour", "Praying", "Caregiver involuntary movements", "Chase and dodge", "No caregiver unusual behaviours", 
                                "Not possible to code caregiver unusual behaviours"]
infant_unusual_behaviours  = ["Frightened Behaviours", "Clingy Behaviours", "Rocking", "Physical tic", "Excessive physical movements", "Infant involuntary movements", 
                             "Hyper-tonality", "Hypo-tonality", "No infant unusual behaviours", "Not possible to code infant unusual behaviours"]
role_reversal              = ["Yes, role reversal", "No role reversal", "Not possible to code role reversal"]
eating                     = ["Yes, eating", "Not eating", "Not possible to code eating"]

# Aggregate all codes into large dictionary
all_codes = [view, audio, alertness_state, 
             caregiver_proximity, caregiver_body_orientation, 
             infant_body_orientation, head_orientation, 
             visual_attention, facial_expression, 
             caregiver_posture, infant_posture, touch_right_hand, 
             touch_left_hand, hand_movements, encouragement,
             agitation_soothing, acknowledgment, 
             physical_imitation, physical_play, rough_and_tumble, 
             caregiver_vocalisation, infant_vocalisation, 
             caregiver_unusual_behaviours, 
             infant_unusual_behaviours, role_reversal, eating]

# Define names of all behavioural groups
all_names = ["view", "audio", "alertness_state", 
             "caregiver_proximity", "caregiver_body_orientation", 
             "infant_body_orientation", "head_orientation", 
             "visual_attention", "facial_expression", 
             "caregiver_posture", "infant_posture", "touch_right_hand", 
             "touch_left_hand", "hand_movements", "encouragement",
             "agitation_soothing", "acknowledgment", 
             "physical_imitation", "physical_play", "rough_and_tumble", 
             "caregiver_vocalisation", "infant_vocalisation", 
             "caregiver_unusual_behaviours", 
             "infant_unusual_behaviours", "role_reversal", "eating"]

#%% Define multi-index for use in creating dataframes 
IDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
var_tup = []

for n in range(len(IDS)):
    c_dat = "dyad" + str(IDs[n])
    
    for i in range(len(all_names)):
        name  = all_names[i]
        codes = all_codes[i]
        for j in range(len(codes)):
           var_tup.append((c_dat, name, codes[j]))

multi_ind = pd.MultiIndex.from_tuples(var_tup)
