# import random

# import pandas as pd
# from faker import Faker


# def generate_data(
#     num_users=100,
#     num_categories=40,
#     fixed_user_categories=10,
#     include_liked=True,
#     output_file="generated_data.csv",
# ):
#     fake = Faker()
#     categories = [f"category_{i}" for i in range(1, num_categories + 1)]
#     data = {
#         "user_name": [f"User_{i}" for i in range(1, num_users + 1)],
#         "categories": [
#             random.sample(categories, fixed_user_categories) for _ in range(num_users)
#         ],
#         "description": [fake.text(max_nb_chars=100) for _ in range(num_users)],
#     }
#     if include_liked:
#         data["liked"] = [random.choice([0, 1]) for _ in range(num_users)]

#     df = pd.DataFrame(data)
#     print("Сгенерированные данные пользователей:")
#     print(df.head())

#     df.to_csv(output_file, index=False)
#     print(f"\nДанные сохранены в файл '{output_file}'.")

#     return df, categories
