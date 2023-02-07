from app import app
from views import AdvertisementView


app.add_url_rule("/advertisements/", view_func=AdvertisementView.as_view("advertisements"),
                 methods=["POST"])
app.add_url_rule("/advertisements/<int:advertisement_id>",
                 view_func=AdvertisementView.as_view("adverts_get"),
                 methods=["GET", "PATCH", "DELETE"])

if __name__ == '__main__':
    app.run()
