from flask import current_app
from flask_restx import Resource, Namespace
from api.api_models import MobileEndpoint

from api.DataAccessObject.User import User
from api.DataAccessObject.Color import Color
from api.DataAccessObject.Exhibition import Exhibition
from api.DataAccessObject.Manual import Manual
from api.DataAccessObject.Material import Material
from api.DataAccessObject.Merchant import Merchant
from api.DataAccessObject.Image import Image
from api.DataAccessObject.Article import Article
from api.DataAccessObject.Window import Window
from api.DataAccessObject.Securit5Shutters import Securit5Shutters
from api.DataAccessObject.RollingShutter import RollingShutter
from api.DataAccessObject.PlisseWire import PlisseWire
from api.DataAccessObject.Kitchen import Kitchen
from api.DataAccessObject.FoldingSecurit import FoldingSecurit

# Responce("", mimeype="application/json")
ns = Namespace(name="mobile")

@ns.route('/relation')
class Mobile(Resource):

    # @ns.expect(MobileEndpoint)
    def post(self):
        relation = ns.payload['relation_type'].lower()
        if relation == 'created_plissewire':
            dao = PlisseWire(current_app.driver)
            plisseWire = dao.newService(ns.payload['device_id'], 
            ns.payload['data']['open_horizontal'],
            ns.payload['data']['two_shutter'],
            ns.payload['data']['piece_count'],
            ns.payload['data']['width'],
            ns.payload['data']['height'],
            ns.payload['date'])
            return plisseWire, 201
            
        elif relation == 'created_window':
                dao = Window(current_app.driver)
                window = dao.newService(ns.payload['device_id'],
                    ns.payload['data']['Wtype'],
                    ns.payload['data']['height'],
                    ns.payload['data']['width'],
                    ns.payload['data']['piece_count'],
                    ns.payload['data']['horizontal'],
                    ns.payload['data']['Gstyle'],
                    ns.payload['data']['Gsingle'],
                    ns.payload['data']['Gthick'],
                    ns.payload['data']['Stype'],
                    ns.payload['data']['Ssub_type'],
                    ns.payload['data']['Sbar_type'],
                    ns.payload['data']['Sbar_type'],
                    ns.payload['data']['Sbar_value'],
                    ns.payload['data']['Ssouas'],
                    ns.payload['data']['SHtype'],
                    ns.payload['data']['SHshutter_count'],
                    ns.payload['data']['SHshape'],
                    ns.payload['data']['FSHposition'],
                    ns.payload['data']['FSHdimension'],
                    ns.payload['date'],
                    )
                return window, 201
            
        elif relation == 'created_securit5shutters':
                dao = Securit5Shutters(current_app.driver)
                securit5Shutters = dao.newService(ns.payload['device_id'] ,
                                                  ns.payload['data']['height'],
                                                  ns.payload['data']['width'],
                                                  ns.payload['data']['piece_count'],
                                                  ns.payload['date'])
                return securit5Shutters, 201
            
        elif relation == 'created_rollingshutter':
            dao = RollingShutter(current_app.driver)
            rollingShutter = dao.newService(ns.payload['device_id'] ,
                                            ns.payload['data']['type'],
                                            ns.payload['data']['height'],
                                            ns.payload['data']['width'],
                                            ns.payload['data']['piece_count'],
                                            ns.payload['date'],
                                            )
            return rollingShutter, 201
        
        elif relation == 'created_kitchen':
            dao = Kitchen(current_app.driver)
            kitchen = dao.newService(ns.payload['device_id'] ,
                                    ns.payload['data']['type'],
                                    ns.payload['data']['height'],
                                    ns.payload['data']['width'],
                                    ns.payload['data']['piece_count'],
                                    ns.payload['date']
                                    )
            return kitchen, 201
        
        elif relation == 'created_foldingsecurit':
            dao = FoldingSecurit(current_app.driver)
            foldingSecurit = dao.newService(ns.payload['device_id'],
                                            ns.payload['data']['sink'],
                                            ns.payload['data']['height'],
                                            ns.payload['data']['width'],
                                            ns.payload['data']['piece_count'],
                                            ns.payload['date'])
            return foldingSecurit, 201
            
        elif relation == 'viewed_gallery':
            dao = Exhibition(current_app.driver)

            exhbition = dao.NewViewedGallery(ns.payload['device_id'] ,
                                             ns.payload['data']['Exhbition_id'],
                                             ns.payload['date'])
                                             
            return exhbition, 201
        
        elif relation == 'create_user':
            dao = User(current_app.driver)

            user = dao.addUser(ns.payload['device_id'] ,
                               ns.payload['data']['type'],
                               ns.payload['date'])
            return user, 201
        
        elif relation == 'selected_color':
            dao = Color(current_app.driver)

            color = dao.NewSelectedColor(ns.payload['device_id'] ,
                                         ns.payload['data']['code'],
                                         ns.payload['data']['type'],
                                         ns.payload['date'])
            return color, 201
        
        elif relation == 'visited_manual':
            dao = Manual(current_app.driver)

            manual = dao.newVisit(ns.payload['device_id'] ,
                                  ns.payload['data']['name'],
                                  ns.payload['data']['type'],
                                  ns.payload['date'])
            return manual, 201
        
        elif relation == 'select_material':
            dao = Material(current_app.driver)

            material = dao.newSelection(ns.payload['device_id'] ,
                                        ns.payload['data']['name'],
                                        ns.payload['date'])
            return material, 201
        
        elif relation == 'create_merchant':
            dao = Merchant(current_app.driver)

            merchant = dao.newViewedMerchantGallery(ns.payload['device_id'] ,
                                            ns.payload['data']['name'],
                                            ns.payload['data']['address'],
                                            ns.payload['data']['contact'],
                                            ns.payload['data']['comertial_activity'],
                                            ns.payload['date'])
            return merchant, 201
        
        elif relation == 'user_click':
            dao = Image(current_app.driver)

            image = dao.newClick(ns.payload['device_id'] ,
                                 ns.payload['data']['url'],
                                 ns.payload['date'])
            return image, 201
        
        elif relation == 'viewed_article':
            dao = Article(current_app.driver)

            artical = dao.NewViewedArticle(ns.payload['device_id'] ,
                                           ns.payload['data']['Exhbition_id'],
                                           ns.payload['date'])
            return artical, 201
       