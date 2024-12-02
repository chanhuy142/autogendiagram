import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches


def draw_ovals(ax, x, y, branches):
    branch_distance = 40
    maxy = y + (len(branches) - 1) * branch_distance  
    for i, branch in enumerate(branches):
       
        branch_y = y + (i * branch_distance)  

       
        oval_width = 80
        
        
        if len(branch) > 10:
            oval_width = 80 + (len(branch) - 10) * 5
        oval_height = 35
        oval = patches.Ellipse((x, branch_y), width=oval_width, height=oval_height, edgecolor='black', facecolor='lightblue', lw=2)
        ax.add_patch(oval)

        #calculate the middle point of y axis of all the ovals
        middle_y = (y + maxy) / 2
        #draw a line from the oval to the middle point of y axis of all the ovals
        ax.plot([x+oval_width/2, x+120], [branch_y, middle_y], color='black', lw=1)
        #draw a line from the middle point of y axis of all the ovals to the middle point of y axis of all the ovals
        



        
        ax.text(x, branch_y, branch, ha='center', va='center', fontsize=10, color='black', zorder=10)


def create_ovals_from_excel(file_path, output_folder='output_images'):
 
    df = pd.read_excel(file_path, header=None) 
    
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
   
    grouped = []
    current_person = None
    branches = []
    
    
    for index, row in df.iterrows():
        person = row[0]
        branch = row[1]
        
        if pd.notna(person): 
            if current_person is not None:
                
                grouped.append((current_person, branches))
            
            
            current_person = person
            branches = [branch] 
        elif pd.notna(branch): 
            branches.append(branch)  
    
    
    if current_person is not None:
        grouped.append((current_person, branches))
    
    
    for i, (name, branches) in enumerate(grouped):
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        ax.set_xlim(0, 250)
        ax.set_ylim(-100, 300)
        
       
        x = 100 
        y = 0 
        
        
        draw_ovals(ax, x, y, branches)
        #hide the axis
        ax.axis('off')
        
        
        output_file = os.path.join(output_folder, f"{name}.png")
        fig.savefig(output_file, bbox_inches='tight', transparent=True)  
        plt.close(fig) 

# read file path from config.txt
with open('config.txt', 'r') as file:
    file_path = file.read().replace('\n', '')
    print(file_path)

create_ovals_from_excel(file_path)