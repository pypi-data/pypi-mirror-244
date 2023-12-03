from envs import DiseaseTreatmentEnv
from policies import StandardOfCare, ClinicalTrial
import numpy as np
import h5py

# Initialize environment
env = DiseaseTreatmentEnv()

# Choose the policy type here based on your needs
# policy = StandardOfCare(env, verbose=True)
policy = ClinicalTrial(env, verbose=True)

num_episodes = 65536  # Number of episodes you want to run
data = {
    'observations': [],
    'actions': [],
    'rewards': [],
    'terminals': [],
    'next_observations': []
}

for episode in range(num_episodes):
    obs = env.reset()
    done = False
    while not done:
        # Use the get_treatment method from the chosen policy
        action = policy.get_treatment(env.current_disease, env.visit_number)
        next_obs, reward, done, _ = env.step(action)
        
        data['observations'].append(obs)
        data['actions'].append(action)
        data['rewards'].append(reward)
        data['terminals'].append(done)
        if not done:
            data['next_observations'].append(next_obs)
        else:
            # Handle the final observation for terminal states
            data['next_observations'].append(obs)  # could use a placeholder or the current obs

        obs = next_obs  # Update the current observation

# Convert lists to numpy arrays
for key in data:
    data[key] = np.array(data[key])

# Save the data as an HDF5 file
with h5py.File('disease_treatment_dataset.hdf5', 'w') as f:
    for key, value in data.items():
        f.create_dataset(key, data=value)
