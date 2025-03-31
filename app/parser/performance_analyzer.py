def flag_heavy_queries(df):
    def is_heavy(row):
        return (
            row["tb_processed"] > 0
            or row["duration_seconds"] > 4
            or row["slot_seconds"] > 1000
        )

    df["is_heavy"] = df.apply(is_heavy, axis=1)
    return df[df["is_heavy"] == True]
