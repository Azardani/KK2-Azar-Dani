def get_summary(df):

    average_price = float(df["Price"].mean())
    average_mileage = float(df["Mileage"].mean())
    average_year = float(df["Year"].mean())

    most_expensive = (
        df.loc[df["Price"].idxmax()]
        .to_dict()
    )

    cheapest = (
        df.loc[df["Price"].idxmin()]
        .to_dict()
    )

    newest = (
        df.loc[df["Year"].idxmax()]
        .to_dict()
    )

    oldest = (
        df.loc[df["Year"].idxmin()]
        .to_dict()
    ) 

    most_miles = (
        df.loc[df["Mileage"].idxmax()]
        .to_dict()
    )

    least_miles = (
        df.loc[df["Mileage"].idxmin()]
        .to_dict()
    )



    return {
        "average_price": average_price,
        "average_mileage": average_mileage,
        "average_year": average_year,
        "most_expensive": most_expensive,
        "cheapest": cheapest,
        "newest": newest,
        "oldest": oldest,
        "most_miles": most_miles,
        "least_miles": least_miles
    }