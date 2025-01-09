from uuid import UUID

from fastapi import HTTPException

from main import app
from src.recomendations import generate_user_vector, recommend_partners, extract_keywords


class ReccomendUsersService:
    def __init__(self):
        self.rf_model = app.state.model
        self.df_all_users = app.state.df_all_users
        self.all_categories = app.state.all_categories

    async def reccomend_users(self, current_user_data: dict) -> list:
        """
        Reccomends users to the current user based on their data.
        params:
            current_user_data: dict
                The data of the current user
        returns:
            list: The list of reccomendations and their scores in percentage
        raises:
            HTTPException: If the model is not trained
        """
        if not self.rf_model:
            raise HTTPException(status_code=400, detail="Model is not trained", all_categories=...)
        try:
            if self.rf_model is None or self.df_all_users is None:
                raise HTTPException(400, "No model or df loaded. Please /upload-dataset first.")

            user_id = data["user_id"]
            user_description = data["description"]
            user_categories = data["categories"]
            viewed = data.get("viewed_users", [])

            # 1) генерим вектор
            current_user_vector = generate_user_vector(user_categories, all_categories)

            # 2) Фильтруем df_all, исключая viewed + самого user_id (если user_id есть в df) (ебать вот это синтаксис)
            df_candidates = df_all[~df_all["user_id"].isin([user_id] + viewed)]

            # 3) берем other_descriptions
            other_descriptions = df_candidates["description"].tolist()

            keywords = extract_keywords(user_description, other_descriptions, top_n=top_n)

            # 4) делаем recommend_partners
            recs = recommend_partners(
                rf_model=rf_model,
                other_users_df=df_candidates,
                current_user_vector=current_user_vector,
                current_user_description=user_descr,
                other_descriptions=other_descriptions,
                keywords=keywords,
            )

            # recs = [(idx, cat_score, text_score, final_score), ...] (зависит от вашей реализации)
            output = []
            for idx, cat_s, txt_s, fs in recs:
                row = df_candidates.iloc[idx]
                output.append(
                    {
                        "user_id": row["user_id"],
                        "cat_score": cat_s,
                        "text_score": txt_s,
                        "final_score": fs,
                    }
                )
            return output
        except:
            raise HTTPException(status_code=500, detail="Internal server error")
