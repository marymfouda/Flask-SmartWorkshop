from flask_restx import  fields
from api import api

UserID = api.model('User Id',
                    {
                        'device_id' : fields.String(required=True),
                    })

UserNodeCreation = api.inherit('User Node', UserID,
                          {
                              'type' : fields.String(required=True)
                          })

AdminRegister = api.model('Admin',
                           {
                               'userName' : fields.String(required=True),
                               'password' : fields.String(required=True)
                           })

#### Services
BaseServiceNode = api.model('Base Service Node',
                            {
                                'type' : fields.String(required=True)
                            })

BaseService = api.inherit('Base Service', UserID,
                            {
                               'height' : fields.Integer(required=True),
                               'width' : fields.Integer(required=True),
                               'piece_count' : fields.Integer(required=True),
                               'date' : fields.DateTime(required=True)
                            })

RollingShutterNode = api.inherit('Rolling Shutter Node', BaseServiceNode)

RollingShutterService = api.inherit('Rolling Shutter Service', BaseService, BaseServiceNode)

SecuritService = api.inherit('Securit 5 Shutters Service', BaseService, {})

FoldingSecuritService = api.inherit('Folding Securit Service', BaseService,
                           {
                               'sink' : fields.Boolean(required=True),
                           })

PlisseWireNode = api.model('Plisse Wire Node', BaseServiceNode)

PlisseWireService = api.inherit('Plisse Wire Service', BaseService, BaseServiceNode,
                           {
                               'two_shutter' : fields.Boolean(required=True),
                               'open_horizontal' : fields.Boolean(required=True),
                           })

WindowNode = api.model('Window Node',  BaseServiceNode)

WindowService = api.inherit('Window Service', BaseService,
                           {
                            'Wtype' : fields.String(required=True),
                            'horizontal' : fields.Boolean(required=True),
                            'Gstyle' : fields.String(required=True), 
                            'Gsingle' : fields.Boolean(required=True), 
                            'Gthick' : fields.Float(required=True),    
                            'Stype' : fields.String(required=True), 
                            'Ssub_type' : fields.String(required=True), 
                            'Sbar_type' : fields.String(required=True), 
                            'Sbar_value' : fields.Float(required=True), 
                            'Ssouas' : fields.String(required=True),
                            'SHtype' : fields.String(required=True), 
                            'SHshutter_count' : fields.Integer(required=True), 
                            'SHtrack_count' : fields.Integer(required=True), 
                            'SHshape' : fields.String(required=True),
                            'FSHposition' : fields.String(required=True), 
                            'FSHdimension' : fields.Float(required=True)
                           })

KitchenNode = api.model('Kitchen Node',  BaseServiceNode)
KitchenService = api.inherit('Kitchen Service', UserID,
                           {
                            'type' : fields.String(required=True),
                            'height' : fields.Integer(required=True),
                            'width' : fields.Integer(required=True), 
                            'depth' : fields.Integer(required=True), 

                            'date' : fields.String(required=True),

                            'shutter_color_type' : fields.String(required=True),    
                            'shelves_number' : fields.Integer(required=True), 
                            'alumetal_unit_type' : fields.String(required=True), 
                            
                            'assembly' : fields.String(required=True),    
                            'unit_assembly' : fields.String(required=True), 
                            'drawer_assembly' : fields.String(required=True), 
                            'drosal_installation' : fields.String(required=True), 
                            
                            'kitchen_sector' : fields.String(required=True), 
                            'shelf_sector' : fields.String(required=True),
                            'shutter_sector' : fields.String(required=True), 
                            'depth_sector' : fields.String(required=True), 
                            
                            'kitchen_unit_position' : fields.String(required=True), 
                            'kitchen_unit_name' : fields.String(required=True)
                           })

#### Nodes
ColorCreation = api.model('Color Node',
                          {
                              'code' : fields.Integer(required=True),
                              'type' : fields.String(required=True)
                          })
ColorSelected = api.inherit('Selected Color',ColorCreation, UserID)

EventCreation = api.model('Event Node',
                          {
                              'keys' : fields.Integer(required=True)
                          })
ArticleCreation = api.model('Article Node',
                          {
                              'title' : fields.String(required=True),
                              'text' : fields.String(required=True)      
                          })
ArticleViewed = api.inherit('Article Viewed',ArticleCreation, UserID)

ExhibitionCreation = api.model('Exhibition Node',
                          {
                              'name' : fields.String(required=True),
                              'description' : fields.String(required=True),
                              'contact' : fields.String(required=True),
                              'address' : fields.String(required=True),
                              'social' : fields.String(required=True),
                              'rate' : fields.Float(required=True),
                          })

ExhibitionViewed = api.inherit('Exhibition Viewed',ExhibitionCreation, UserID)

GalleryCategoryCreation = api.model('Gallery Category Node',
                          {
                              'name' : fields.String(required=True),
   
                          })
ImageNodeCreation = api.model('Image Node',
                          {
                              'url' : fields.String(required=True),
   
                          })
ImageClicked = api.inherit('Image Clicked', ImageNodeCreation, UserID)
ManualCreation = api.model('Manual Node',
                          {
                              'name' : fields.String(required=True),
                              'type' : fields.String(required=True)  
                          })
ManualVisited = api.inherit('Manual Visited', UserID, ManualCreation)
MaterialCreation = api.model('Matrial Node',
                          {
                            'name' : fields.String(required=True),
                          })
MaterialSelected = api.inherit('Material Selected', UserID, MaterialCreation)
MerchantNodeCreation = api.model('Merchant Node',
                          {
                              'name' : fields.String(required=True),
                              'comertial_activity' : fields.String(required=True) , 
                              'contact' : fields.String(required=True) , 
                              'address' : fields.String(required=True)  
                          })
MerchantRelations = api.inherit('Merchant Relations', UserID, MerchantNodeCreation)

#### Single Endpoint
BaseMobile = api.model('BaseMobile' ,
                        {
                         'relation_type' : fields.String(required=True),
                         'service' : fields.String(required=True)
})
MobileEndpoint = api.inherit('Mobile Endpoint',BaseMobile , WindowService, PlisseWireService, FoldingSecuritService,
                             SecuritService, MerchantRelations , MaterialSelected , ManualVisited , ImageClicked,
                             GalleryCategoryCreation , ExhibitionViewed , ArticleViewed , ColorSelected )