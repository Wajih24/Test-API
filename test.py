from django.http import response
import requests 

Base = "http://127.0.0.1:5000/"

'''response = requests.get(Base + "train")
print(response.json())'''

a = {'id': 1677.0,
 'level_id': 3.0,
 'total_time': '00:06:07',
 'donuts': 20.0,
 'candy': 350.0,
 'level': 1.0,
 'progress': 0.0,
 'nbr Items': 0.0,
 'perseverance badge': 0.0,
 'concentration': 0.0,
 'Success': 0.0,
 'Excellence': 0.0,
 'Upgrade': 0.0,
 'total_Time_Education': 1764.0,
 'nb_mistakes': 0.0,
 'correct Question': 10.0,
 'correct_Q_Math': 0.0,
 'correct_Q_Science': 10.0,
 'correct_Q_Ar': 0.0,
 'correct_Q_Fr': 0.0,
 'Q_Best_Time': 5.0,
 'best_time_math': 0.0,
 'best_time_science': 5.0,
 'best_time_ar': 0.0,
 'best_time_fr': 0.0,
 'Q_Worst_Time': 0.0,
 'worst_time_math': 0.0,
 'worst_time_science': 0.0,
 'worst_time_ar': 0.0,
 'worst_time_fr': 0.0,
 'Q_Avg_Time': 5,
 'Avg_Time_math': 0,
 'Avg_Time__science': 5,
 'Avg_Time_ar': 0,
 'Avg_Time_fr': 0,
 'count ex not completed': 6.0}

response = requests.post(Base + "predict",json=a)

print(response.json())