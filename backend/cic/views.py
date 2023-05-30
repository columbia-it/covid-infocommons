from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from apis.models import Grant, Person, Asset

states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"    
    }

def index(request):
    """Home view callable, for the home page."""
    return render(request, 'grants/index.html', {'keywords': request.GET.get('keywords', '')})


def detail(request, grant_id):
    grant = get_object_or_404(Grant, pk=grant_id)
    state_abbrev = ""
    state = ""
    keyword = request.GET.get('keyword', '')
    if grant.awardee_organization is not None:
        state_abbrev = grant.awardee_organization.state
    if state_abbrev in states:
        state = states[state_abbrev]        
    return render(request, 'grant_detail.html', {'grant': grant, 'state': state, 'keyword': keyword})

def pi_detail(request, pi_id): 
    keyword = request.GET.get('keyword', '')
    person = get_object_or_404(Person, pk=pi_id)
    grants = Grant.objects.filter(principal_investigator__id=pi_id)
    assets = Asset.objects.filter(author__id=pi_id)
    videos = []
    profile_pic = None
    for asset in assets:
        if asset.filename == 'profile_image':
            profile_pic = asset.download_path
        elif asset.filename == 'cic_video':
            videos.append(asset.download_path)
    return render(request, 'person_detail.html', {'person': person, 'grants': grants, 'keyword': keyword, 'profile_pic': profile_pic, 'videos': videos })
