
Many of the APIs will allow a "filter" to select a single known item by an identifier other than the CIC ID.

Organizations by ROR:
- filter by a single ROR
  `/v1/organizations?filter[ror]=https://ror.org/008rp3t36`
- filter by multiple RORs 
  `/v1/organizations?filter[ror.in]=https://ror.org/008rp3t36,https://ror.org/05skzv947`

People by ORCID or email:
- filter by single ORCID
  `/v1/people?filter[orcid]=http://orcid.org/0000-0002-1825-0097`
- filter by multiple ORCIDs
  `/v1/people?filter[orcid.in]=http://orcid.org/0000-0003-1989-0090,http://orcid.org/0002-0013-1909-0091`
- filter by emails
  `/v1/people?filter[emails.icontains]=RandyMCrichton@rhyta.com`


Grants are currently located via the search API. Grants by grant ID:
- https://cice-dev.paas.cc.columbia.edu/search/grants?keyword=3R01AI072726-10S1
