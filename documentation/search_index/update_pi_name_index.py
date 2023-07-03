from opensearchpy import OpenSearch, RequestsHttpConnection

def main():
    host = '<VPC_DOMAIN_ENDPOINT>'
    
    client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        use_ssl = True,
        verify_certs = True)
    
    body = {
        "size":7000, "from": 0,
        "query": { 
            "bool": { 
                "must": []
            }
        }
    }
    
    response = client.search(index="grant_index", body=body)
    print('Total Documents = {}'.format(response['hits']['total']))

    all_documents = response['hits']['hits']
    documents = []
    
    for num, doc in enumerate(all_documents):
        documents += [doc['_id']]
    pi_with_full_names = 0
    pi_with_no_full_names = 0
   
    for num, doc_id in enumerate(documents):
        b = {
            'size': 10000, 'from': 0,
            'query': {
                'match': {
                    "id": doc_id
                }
            }
        }
        
        r = client.search(index="grant_index", body=b)
        temp_pi =  r['hits']['hits'][0]['_source']['principal_investigator']
        
        if not temp_pi.get('full_name', None):
            print('No Full name')
            updated_grant = {
                "doc": { 
                    "principal_investigator": {
                        "full_name": temp_pi.get('first_name') + ' ' + temp_pi.get('last_name')
                    }
                }
            }
            pi_with_no_full_names = pi_with_no_full_names + 1
            update_resp = client.update(index='grant_index', id=doc_id, body=updated_grant)

        else:
            print(r['hits']['hits'][0]['_source']['principal_investigator'].get('full_name', None))
            pi_with_full_names = pi_with_full_names + 1
    
    

if __name__=="__main__":
    main()
