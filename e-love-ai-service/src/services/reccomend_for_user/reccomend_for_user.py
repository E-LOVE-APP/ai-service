from fastapi import HTTPException
from src.recomendations import extract_keywords, generate_user_vector, recommend_partners


class ReccomendUsersService:
    """
    Service that uses a pre-learned model, dataframe with all users information,
    and categories information from our main business logic.
    """

    def __init__(self, rf_model, df_all_users, all_categories):
        self.rf_model = rf_model
        self.df_all_users = df_all_users
        self.all_categories = all_categories

    async def reccomend_users(self, current_user_data: dict) -> list:
        if not self.rf_model:
            raise HTTPException(status_code=400, detail="Model is not trained")
        try:
            if self.rf_model is None or self.df_all_users is None:
                raise HTTPException(400, "No model or df loaded. Please /upload-dataset first.")

            user_id = current_user_data["user_id"]
            user_description = current_user_data["description"]
            user_categories = current_user_data["categories"]
            viewed = current_user_data.get("viewed_users", [])

            # Генерируем вектор для текущего пользователя
            current_user_vector = generate_user_vector(user_categories, self.all_categories)

            # Проверка наличия столбца 'candidate_user_id' и фильтрация DataFrame
            if "candidate_user_id" not in self.df_all_users.columns:
                raise HTTPException(400, "'candidate_user_id' column not found in dataframe")
            df_candidates = self.df_all_users[
                ~self.df_all_users["candidate_user_id"].isin([user_id] + viewed)
            ]

            # Ограничим количество кандидатов (например, первыми 1000)
            df_candidates = df_candidates.head(10000)

            # Берём описания других пользователей
            other_descriptions = df_candidates["description"].tolist()

            top_n = 5  # задаем нужное значение
            keywords = extract_keywords(user_description, other_descriptions, top_n=top_n)

            recs = recommend_partners(
                model=self.rf_model,
                other_users_df=df_candidates,
                current_user_vector=current_user_vector,
                current_user_description=user_description,
                other_descriptions=other_descriptions,
                keywords=keywords,
            )

            print("recs: ", recs)

            output = []
            # for idx, cat_s, txt_s, fs in recs:
            #     row = df_candidates.iloc[idx]
            #     output.append(
            #         {
            #             "user_id": row["candidate_user_id"],
            #             "cat_score": cat_s,
            #             "text_score": txt_s,
            #             "final_score": fs,
            #         }
            #     )
            for idx, cat_s, txt_s, fs in recs:
                row = df_candidates.iloc[idx]
                output.append(
                    {
                        "user_id": row["candidate_user_id"],
                        "cat_score": float(cat_s),  # преобразование к float
                        "text_score": float(txt_s),  # преобразование к float
                        "final_score": float(fs),  # преобразование к float
                    }
                )

            print("output_data: ", output)
            return output
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
