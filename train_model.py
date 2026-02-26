import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# --------- DATASET ---------
data = {
    'sleep_hours': [4,5,6,7,8,3,5,6,7,4,8,2,6,7,5],
    'study_hours': [8,7,6,5,4,9,7,6,5,8,3,10,6,5,7],
    'screen_time': [8,7,6,5,4,9,7,6,5,8,3,10,6,5,7],
    'social_activity': [1,2,3,4,5,1,2,3,4,1,5,1,3,4,2],
    'stress_level': [
        'High','High','Medium','Low','Low',
        'High','High','Medium','Low','High',
        'Low','High','Medium','Low','High'
    ]
}

df = pd.DataFrame(data)

# Convert labels to numbers
df['stress_level'] = df['stress_level'].map({'Low':0,'Medium':1,'High':2})

X = df[['sleep_hours','study_hours','screen_time','social_activity']]
y = df['stress_level']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open('stress_model.pkl','wb'))

print("Model trained and saved as stress_model.pkl")