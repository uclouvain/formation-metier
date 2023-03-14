from django.contrib.auth import views as auth_views
from django.urls import path, include
from schema_graph.views import Schema

from formation_metier.api import urls_api
from formation_metier.views import ListeFormationView, HomeView, NouvelleFormationFormView, DetailFormation, \
    DetailSeanceView, ModificationFormationView, ModificationSeanceView, NouvelleSeanceFormView, SuppressionSeance, \
    SuppressionFormation, SelectionParticipantAutoComplete, SuppressionMultiplesInscriptionsParFormateur, \
    SuppressionInscriptionParParticipant, InscriptionFormationPourParticipant, InscriptionSeancePourParticipantView, \
    SuppressionUniqueInscriptionParFormateurView, ListeParticipantsFormationView

app_name = 'formation_metier'
urlpatterns = [
    path('', HomeView.as_view(), name=HomeView.name),

    # list_view
    path('liste_formations/', ListeFormationView.as_view(), name=ListeFormationView.name),
    path('liste_participants/<uuid:formation_id>', ListeParticipantsFormationView.as_view(),
         name=ListeParticipantsFormationView.name),

    # detail_view
    path('formation/<uuid:formation_id>/', DetailFormation.as_view(), name=DetailFormation.name),
    path('formation/seance/<uuid:seance_id>/', DetailSeanceView.as_view(), name=DetailSeanceView.name),

    # new_view
    path('nouvelle_formation/', NouvelleFormationFormView.as_view(), name=NouvelleFormationFormView.name),
    path('formation/nouvelle_seance/<uuid:formation_id>/', NouvelleSeanceFormView.as_view(),
         name=NouvelleSeanceFormView.name),

    # inscription_pour_participant_view
    path('inscription/formation/<uuid:formation_id>/', InscriptionFormationPourParticipant.as_view(),
         name=InscriptionFormationPourParticipant.name),
    path('inscription/seance/<uuid:seance_id>/', InscriptionSeancePourParticipantView.as_view(),
         name=InscriptionSeancePourParticipantView.name),

    # update_view
    path('formation/modification/<uuid:formation_id>/', ModificationFormationView.as_view(),
         name=ModificationFormationView.name),
    path('formation/seance/modification/<uuid:seance_id>/', ModificationSeanceView.as_view(),
         name=ModificationSeanceView.name),

    # delete_view
    path('formation/suppression/<uuid:formation_id>/', SuppressionFormation.as_view(), name=SuppressionFormation.name),
    path('formation/seance/suppression/<uuid:seance_id>/', SuppressionSeance.as_view(), name=SuppressionSeance.name),
    path('formation/seance/inscription_formateur/suppression_multiple/',
         SuppressionMultiplesInscriptionsParFormateur.as_view(),
         name=SuppressionMultiplesInscriptionsParFormateur.name
         ),
    path('formation/seance/inscription_participant/suppression/', SuppressionInscriptionParParticipant.as_view(),
         name=SuppressionInscriptionParParticipant.name),
    path('formation/seance/inscription_formateur/suppression_unique/<uuid:inscription_id>',
         SuppressionUniqueInscriptionParFormateurView.as_view(),
         name=SuppressionUniqueInscriptionParFormateurView.name),

    # Autocomplete Widget

    path('autocompletePerson/', SelectionParticipantAutoComplete.as_view(), name=SelectionParticipantAutoComplete.name),

    # API
    path('', include(urls_api)),

    # auth
    path('accounts/login/', auth_views.LoginView.as_view()),

    # graph_models
    path("schema/", Schema.as_view(), name='schemaModels'),
]
