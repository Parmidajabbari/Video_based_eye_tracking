import csv
import os
import pandas as pd
#TODO add monitor size data if needed
class DataSet:
    def __init__(self, csv_file_path , frames_file_name='images_data.csv', landmarks_file_name='landmarks_data.csv', gazes_file_name='gaze_data.csv'):
        self.csv_file_path = csv_file_path
        self.frames_file_name = frames_file_name
        self.landmarks_file_name = landmarks_file_name
        self.gazes_file_name = gazes_file_name
        self.combine_csv_files()
        self.user_id = self.get_last_user_id() + 1  # Get the last user ID and increment by 1
        
        self.landmarks_list = []
        self.frame_list = []
        self.gaze_list = []

    def get_last_user_id(self):
        combined_df = self.read_combined_csv()
        if 'User_ID' in combined_df.columns:
            last_user_id = combined_df['User_ID'].max()
            if pd.isna(last_user_id):
                return 0
            return int(last_user_id)
        return 0    
    
    def get_curr_user_id(self):
        return self.user_id
    
    def write_to_csv(self, frame_index, frame_path, landmarks, gaze):
        data_list = []

        for frame_index, frame_path in enumerate(photo_dataset):
            landmarks = landmark_dataset[frame_index]  # Assuming landmarks for the same frame are at the same index
            gaze_coordinates = (x, y)  # Replace with the actual gaze coordinates for this frame

            # Create a dictionary for this frame
            frame_data = {
                'frame_index': frame_index,
                'frame_path': frame_path,
                'landmarks': landmarks,
                'gaze': gaze
            }

            # Add the frame data to the list
            data_list.append(frame_data)
            # print(self.landmarks_list)

        # Now 'data_list' contains a list of dictionaries, each representing a frame with its associated data.

            
    def write_frameData_to_csv(self, index, frame_path, landmarks, gaze):
        #consider that frame_path is the path of the image files!
        self.write_framePath_to_csv(index, frame_path)
        self.write_landmarks_to_csv(index, landmarks)
        self.write_gaze_to_csv(index, gaze[0], gaze[1])
        #TODO add log in here

            
    def write_framePath_to_csv(self, index, framePath):
        full_file_path = os.path.join(self.csv_file_path, self.frames_file_name)

        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Frame_path', 'User_ID']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Frame_path', 'User_ID']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Index': index, 'Frame_path': framePath, 'User_ID': self.user_id})
            
    def write_landmarks_to_csv(self, index, landmarks):
        full_file_path = os.path.join(self.csv_file_path, self.landmarks_file_name)
        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Category', 'X', 'Y', 'User_ID']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Category', 'X', 'Y', 'User_ID']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            for category_data in landmarks:
                category_name = category_data['name']
                for x, y in category_data['landmarks']:
                    writer.writerow({'Index': index, 'Category': category_name, 'X': x, 'Y': y, 'User_ID': self.user_id})
                    
    def write_gaze_to_csv(self, index, gaze_x, gaze_y):
        full_file_path = os.path.join(self.csv_file_path, self.gazes_file_name)

        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Gaze_X', 'Gaze_Y', 'User_ID']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Gaze_X', 'Gaze_Y', 'User_ID']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Index': index, 'Gaze_X': gaze_x, 'Gaze_Y': gaze_y, 'User_ID': self.user_id})
            
    def load_by_index(self, index):
        landmarks = []
        with open(os.path.join(self.csv_file_path, self.landmarks_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row['Index']) == index:
                    category = row['Category']
                    x = int(row['X'])
                    y = int(row['Y'])

                    landmarks.append({'category': category, 'x': x, 'y': y})
                    
        return landmarks
    
    def load_frame_from_csv(self):
        frame_data = []
        with open(os.path.join(self.csv_file_path, self.frames_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                index = int(row['Index'])
                frame_path = row['Frame_path']

                gaze_data.append({'index': index, 'path': frame_path})

        self.frame_list = frame_list
        
        return self.frame_list
    
    def load_landmarks_from_csv(self):
        
        landmarks = []
        with open(os.path.join(self.csv_file_path, self.landmarks_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            index_base = 0
            for row in csv_reader:
                index = int(row['Index'])
                category = row['Category']
                x = int(row['X'])
                y = int(row['Y'])
                
                landmarks.append({'index': index, 'category': category, 'x': x, 'y': y})
                
                
        self.landmarks_list = landmarks
        
        return self.landmarks_list
    
    def load_gaze_from_csv(self):
        gaze_data = []
        with open(os.path.join(self.csv_file_path, self.gazes_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                index = int(row['Index'])
                gaze_x = int(row['Gaze_X'])
                gaze_y = int(row['Gaze_Y'])

                gaze_data.append({'index': index, 'gaze_x': gaze_x, 'gaze_y': gaze_y})

        self.gaze_list = gaze_data
        
        return self.gaze_list


    def combine_csv_files(self, output_file_name='combined_data.csv'):
        landmarks_file_path = os.path.join(self.csv_file_path, self.landmarks_file_name)
        gaze_file_path = os.path.join(self.csv_file_path, self.gazes_file_name)

        if not os.path.exists(landmarks_file_path):
            with open(landmarks_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Category', 'Landmark_X', 'Landmark_Y', 'User_ID']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        if not os.path.exists(gaze_file_path):
            with open(gaze_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Gaze_X', 'Gaze_Y', 'User_ID']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        landmarks_df = pd.read_csv(landmarks_file_path)
        gaze_df = pd.read_csv(gaze_file_path)

        # Merge the dataframes based on 'Index'
        combined_df = pd.merge(landmarks_df, gaze_df, on='Index', how='outer')
        # Rename columns to match the specified format
        combined_df.rename(columns={'X': 'Landmark_X', 'Y': 'Landmark_Y', 'Gaze_X': 'Gaze_X', 'Gaze_Y': 'Gaze_Y', 'User_ID_x' : 'User_ID'}, inplace=True)

        # Reorder columns to match the desired format
        combined_df = combined_df[['Index', 'Category', 'Landmark_X', 'Landmark_Y', 'Gaze_X', 'Gaze_Y', 'User_ID']]

        # Save the combined dataframe to a new CSV file
        combined_df.to_csv(os.path.join(self.csv_file_path, output_file_name), index=False)

    def read_combined_csv(self, combined_file_name='combined_data.csv'):
        combined_file_path = os.path.join(self.csv_file_path, combined_file_name)
        combined_df = pd.read_csv(combined_file_path)
        return combined_df

if __name__ == "__main__":
    csv_file_path = '/'  
