from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Update with your Neo4j server URI
username = "neo4j"  # Update with your Neo4j Username
password = "password"  # Update with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

Schema_tree = {
    'User' : {
               'label': 'User',
               'class' : 'node' ,
               'attributes' : {
                   'device_id' : 1
               } },
    'Securit5Shutters' : {
                        'label' : 'Securit5Shutters',
                        'class' : 'node',
                        'attributes' : {
                          } ,},

    'Kitchen' : {       'label' : 'Kitchen',
                        'class' : 'node',
                        'attributes' : {
                            'type' : "'kitchen-8'"
                          } ,},
    'Measurement' : {   'label' : 'Measurement',
                        'class' : 'node',
                        'attributes' : {
                            'insides_panels': "'mm'" ,
                            'main_shutter' : "'hh'" ,
                            'secondary_shutter' :"'uu'" , 
                            'width_of_shutter' : 7,
                            'hight_of_shutter' :8,
                            'inclusion_height' :9,
                            'thickness_panels' :1.1, 
                            'dorsal_condyle' :"'hj'"
                          } ,}, 
    'KitchenUnit' : {   'label' : 'KitchenUnit',
                        'class' : 'node',
                        'attributes' : {
                            'position' : "'left'"
                          } ,}, 
    'Selection' : {     'label' : 'Selection',
                        'class' : 'node',
                        'attributes' : { 
                            'sector_type'  : "'yy'", 
                            'compilation' : "'hh'", 
                            'Drawer_assembly' : "'ll'", 
                            'shelf_sector' : "'nn'", 
                            'depth_sector' : 99, 
                            'Dorsal_installation' : "'kk'" ,
                            'shutter_type' : "'uyt'", 
                            'Unit_assembly' : "'jjj'"
                          } ,},   
    'FoldingSecurit' : {   
                        'label' : 'FoldingSecurit',
                        'class' : 'node',
                        'attributes' : {
                            'id' : 1
                          } ,}, 
    'RollingShutter' : {   
                        'label' : 'RollingShutter',
                        'class' : 'node',
                        'attributes' : {
                            'type' : "'RollingShutter'"
                          } ,}, 
    'Window' : {   
                        'label' : 'Window',
                        'class' : 'node',
                        'attributes' : {
                            'type' : "'Window'"
                          } ,},                      
    'Glass' : {   
                        'label' : 'Glass',
                        'class' : 'node',
                        'attributes' : {
                            'style' : "'Glass'"
                          } ,},                      
    'Shutter' : {   
                        'label' : 'Shutter',
                        'class' : 'node',
                        'attributes' : {
                            'type' : "'Shutter'", 
                            'shutter_count' : 5,
                            'track_count' :6
     } ,},

    'FixedShutter' : {   
                        'label' : 'FixedShutter',
                        'class' : 'node',
                        'attributes' : {
                            'position' : "'right'"
     } ,},  
    'Sector' : {   
                        'label' : 'Sector',
                        'class' : 'node',
                        'attributes' : {
                            'type' : "'Sector'" ,
                            'sub_type': "'sec-type'" ,
                            'key': 99
     } ,}, 
    'PlisseWire' : {   
                        'label' : 'PlisseWire',
                        'class' : 'node',
                        'attributes' : {
                            'sector_type': "'PlisseWire'" 
     } ,},  
    'Article' : {   
                        'label' : 'Article',
                        'class' : 'node',
                        'attributes' : {
                            'title': "'Article'" 
     } ,},  
    'Event' : {   
                        'label' : 'Event',
                        'class' : 'node',
                        'attributes' : {
                            'keys': 8
     } ,},  
    'Manual' : {   
                        'label' : 'Manual',
                        'class' : 'node',
                        'attributes' : {
                            'name': "'Manual'"
     } ,},  
    'Color' : {   
                        'label' : 'Color',
                        'class' : 'node',
                        'attributes' : {
                            'code': 1123
     } ,},  
    'Material' : {   
                        'label' : 'Material',
                        'class' : 'node',
                        'attributes' : {
                            
     } ,}, 
    'Merchant' : {   
                        'label' : 'Merchant',
                        'class' : 'node',
                        'attributes' : {
                            'address' : "'Tanta'" , 
                            'contact_number' :"'0123456789'" ,
                            'comertial_activity' :"'almontal'"  ,
                            'trade_name' :"'mariam'"
     } ,}, 
    'Image' : {   
                        'label' : 'Image',
                        'class' : 'node',
                        'attributes' : {
                            'url': "'url'"
     } ,}, 
    'GalleryCategory' : {   
                        'label' : 'GalleryCategory',
                        'class' : 'node',
                        'attributes' : {
                            'name': "'GalleryCategory'"
     } ,}, 
    'Exhbition' : {   
                        'label' : 'Exhbition',
                        'class' : 'node',
                        'attributes' : {
                            'name' : "'Exhbition'" , 
                            'description' : "'wonderful'" , 
                            'contact_number' :"'0123456789'" , 
                            'address' : "'tanta'", 
                            'social_media' :"'facebook'", 
                            'rate' : 5
     } ,}, 
     
# Relationships
        'CREATED_SERVICE1': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Securit5Shutters',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height' : '367' ,
                'wight' : '8.9',
            }
        },
        'CREATED_SERVICE6': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'PlisseWire',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height' : '367' ,
                'wight' : '8.9',
                'piece_count' : '9'
            }
        },
        'CREATED_SERVICE2': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Kitchen',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height' : '335' ,
                'wight' : '3.9'
            }
        },
          'CREATED_SERVICE3': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'FoldingSecurit',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height': 7, 
                'wight' :78, 
                'piece_count': 7 , 
                'sink_path': 3
            }
        },
        'CREATED_SERVICE4': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'RollingShutter',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height': 7, 
                'wight' :78, 
                'piece_count': 7 
            }
        },
        'CREATED_SERVICE5': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Window',
            'relation': 'CREATED_SERVICE',
            'attributes': {
                'height': 7, 
                'wight' :78, 
                'piece_count': 7 , 
                'horizontal' : "'vetric'"
            }
        },
        
        'HAS_UNIT': {
            'class': 'rel',
            'start_node' : 'Kitchen' , 
            'end_node': 'KitchenUnit',
            'relation': 'HAS_UNIT',
            'attributes': {
                'unit_name' :"'kit8'"
            }
        },
        'HAS_FEATCHER': {
            'class': 'rel',
            'start_node' : 'Kitchen' , 
            'end_node': 'Selection',
            'relation': 'HAS_FEATCHER',
            'attributes': {
                'unit_name' :"'kit8'"
            }
        },
        'HAS_GLASS': {
            'class': 'rel',
            'start_node' : 'Window' , 
            'end_node': 'Glass',
            'relation': 'HAS_GLASS',
            'attributes': {
               'single': "'unit'" ,
               'thickness' : 9
            }
        },
        'HAS_SHUTTER': {
            'class': 'rel',
            'start_node' : 'Window' , 
            'end_node': 'Shutter',
            'relation': 'HAS_SHUTTER',
            'attributes': {
              'shutter_shape' : "'shutter_shape'"
            }
        },
        'HAS_SECTOR': {
            'class': 'rel',
            'start_node' : 'Window' , 
            'end_node': 'Sector',
            'relation': 'HAS_SECTOR',
            'attributes': {
                'bar_type' : "'bar_type'", 
                'bar_value' :"'bar_value'", 
                'souas' :"'souas'"
            }
        },
        'VIEWED_ARTICLE': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Article',
            'relation': 'VIEWED_ARTICLE',
            'attributes': {
                
            }
        },
        'TRIGGERED': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Event',
            'relation': 'TRIGGERED',
            'attributes': {
                
            }
        },
          'FOLLOWED': {
            'class': 'rel',
            'start_node' : 'Event' , 
            'end_node': 'Event',
            'relation': 'FOLLOWED',
            'attributes': {
                
            }
        },
          'VISITED_MANUAL': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Manual',
            'relation': 'VISITED_MANUAL',
            'attributes': {
                
            }
        },
          'CONTAIN_ARTICLE': {
            'class': 'rel',
            'start_node' : 'Manual' , 
            'end_node': 'Article',
            'relation': 'CONTAIN_ARTICLE',
            'attributes': {
                
            }
        },
          'SELECTED_COLOR': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Color',
            'relation': 'SELECTED_COLOR',
            'attributes': {
                
            }
        },
          'SELECTED_COLOR': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Material',
            'relation': 'SELECTED_COLOR',
            'attributes': {
                
            }
        },
          'CONTACTED': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Merchant',
            'relation': 'CONTACTED',
            'attributes': {
                
            }
        },
          'CREATED_MERCHANT': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Merchant',
            'relation': 'CREATED_MERCHANT',
            'attributes': {
                
            }
        },
          'VIEWED_MERCHANT_GALLERY': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Merchant',
            'relation': 'VIEWED_MERCHANT_GALLERY',
            'attributes': {
                
            }
        },
          'CLICKED': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Image',
            'relation': 'CLICKED',
            'attributes': {
                
            }
        },
          'HAS_IMAGE2': {
            'class': 'rel',
            'start_node' : 'GalleryCategory' , 
            'end_node': 'Image',
            'relation': 'HAS_IMAGE',
            'attributes': {
                
            }
        },
          'HAS_IMAGE': {
            'class': 'rel',
            'start_node' : 'Exhbition' , 
            'end_node': 'Image',
            'relation': 'HAS_IMAGE',
            'attributes': {
                
            }
        },
            'VIEWED_GALLERY': {
            'class': 'rel',
            'start_node' : 'User' , 
            'end_node': 'Exhbition',
            'relation': 'VIEWED_GALLERY',
            'attributes': {
                
            }
        },
            'HAS_MEASURE': {
            'class': 'rel',
            'start_node' : 'Kitchen' , 
            'end_node': 'Measurement',
            'relation': 'HAS_MEASURE',
            'attributes': {
                
            }
        },
            'HAS_COLOR': {
            'class': 'rel',
            'start_node' : 'Kitchen' , 
            'end_node': 'Color',
            'relation': 'HAS_COLOR',
            'attributes': {
                
            }
        },
            'HAS_COLOR': {
            'class': 'rel',
            'start_node' : 'Kitchen' , 
            'end_node': 'Color',
            'relation': 'HAS_COLOR',
            'attributes': {
                
            }
        },
            
            'HAS_COLOR': {
            'class': 'rel',
            'start_node' : 'Material' , 
            'end_node': 'Color',
            'relation': 'HAS_COLOR',
            'attributes': {
                
            }
        },
          
            'HAS_FIXED': {
            'class': 'rel',
            'start_node' : 'Shutter' , 
            'end_node': 'FixedShutter',
            'relation': 'HAS_FIXED',
            'attributes': {
            
            }
        },
            
}

def execute_command(query):
    with driver.session() as session:
        session.run(query)


for key in Schema_tree:
    class_type = Schema_tree[key]['class']
    if class_type == 'node':
        label = Schema_tree[key]['label']
        attributes = Schema_tree[key]['attributes']
        attribute_str = ', '.join([f"{k}: {v}" for k, v in attributes.items()])
        create_query = f"MERGE (: {label} {{ {attribute_str} }})"
        execute_command(create_query)
    elif class_type == 'rel': 
        start_node = Schema_tree[key]['start_node']
        end_node = Schema_tree[key]['end_node']
        relation = Schema_tree[key]['relation']
        attributes = Schema_tree[key]['attributes']
        attribute_str = ', '.join([f"{k}: {v}" for k, v in attributes.items()])
        match_query = f"MATCH (start: {start_node}), (end: {end_node}) " \
                      f"MERGE (start)-[: {relation} {{ {attribute_str} }}]->(end)"
        execute_command(match_query)
driver.close()
# print(len(Schema_tree.keys()))
print(match_query)