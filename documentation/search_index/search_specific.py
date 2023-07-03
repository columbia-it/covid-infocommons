from opensearchpy import OpenSearch
import json

def main():
    host = '<VPC_DOMAIN_ENDPOINT>'

    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        # http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
    )
    query_body = {
      "query": {
            "match": {
                "principal_investigator.id": 24773
            }
        }
     }
    

    response = client.search(index="grant_index", body=query_body)
    print(response['hits'])

if __name__=="__mai
