from django.shortcuts import render, redirect
from django.http import HttpResponse
from .generate_csv import process_file
import matplotlib.pyplot as plt
import os

GLOBAL_DF = None

def home(request):
    global GLOBAL_DF

    if request.method == "POST":
        file = request.FILES.get("file")

        if file:
            result = process_file(file)

            if result:
                df, total, best = result
                GLOBAL_DF = df

                # Graph
                plt.figure()
                plt.bar(df["ID"], df["CA_Net"])
                path = "media/chart.png"
                plt.savefig(path)
                plt.close()

                request.session["total"] = float(total)
                request.session["best"] = best

                return redirect("dashboard")

    return render(request, "ventes/home.html")


def dashboard(request):
    global GLOBAL_DF

    if GLOBAL_DF is None:
        return redirect("home")

    context = {
        "table": GLOBAL_DF.to_html(classes="table table-striped"),
        "total": request.session.get("total"),
        "best": request.session.get("best"),
        "chart": "/media/chart.png"
    }

    return render(request, "ventes/dashboard.html", context)


def download_file(request):
    global GLOBAL_DF

    if GLOBAL_DF is None:
        return HttpResponse("Aucun fichier")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resultats.csv"'
    GLOBAL_DF.to_csv(response, index=False)

    return response