import base64

from huza.icons.images.img import image_dict
from PyQt5 import QtGui, QtCore

from huza.icons.images.img1 import image_dict1
from huza.icons.images.img3 import image_dict3


class IconFile(object):
    data: bytes = None
    filetype: str = None


class IconHandlerBase:
    name = ''

    def __init__(self):
        self._qicon_cache = {}
        self._icon_database = {}
        self._qpixmap_cache = {}

    def _set_img_database(self, img_data_base):
        self._icon_database.update(img_data_base)

    def get_icon_bytes(self, attr):
        if self._icon_database.get(attr) is None:
            return None
        icon_from_db = self._icon_database.get(attr)
        len_icon_db = len(icon_from_db)
        if len_icon_db < 3:
            data, filetype = icon_from_db
            ifile = IconFile()
            ifile.data = base64.b64decode(bytes(data, encoding='utf-8'))
            ifile.filetype = filetype
            return ifile
        else:
            data, filetype, data2 = icon_from_db
            ifile = IconFile()
            ifile.data = base64.b64decode(bytes(data, encoding='utf-8'))
            ifile.filetype = filetype
            return ifile

    def __getattr__(self, attr):
        if self._icon_database.get(attr) is not None:
            icon_from_db = self._icon_database[attr]
            len_icon_db = len(icon_from_db)
            if len_icon_db < 3:
                data, filetype = icon_from_db
                try:
                    return self._qicon_cache[attr]
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap.fromImage(
                        QtGui.QImage().fromData(QtCore.QByteArray.fromBase64(bytes(data, encoding='utf-8')),
                                                format=filetype)))
                    self._qicon_cache[attr] = icon
            else:
                data, filetype, data2 = icon_from_db
                try:
                    return self._qicon_cache[attr]
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap.fromImage(
                        QtGui.QImage().fromData(QtCore.QByteArray.fromBase64(bytes(data, encoding='utf-8')),
                                                format=filetype)))
                    icon.addPixmap(QtGui.QPixmap.fromImage(
                        QtGui.QImage().fromData(QtCore.QByteArray.fromBase64(bytes(data2, encoding='utf-8')),
                                                format=filetype)),
                        state=QtGui.QIcon.On)
                    self._qicon_cache[attr] = icon

            return icon
        return None


class IconHandler(IconHandlerBase):
    def get_picmap(self, attr):
        if self._icon_database.get(attr) is not None:
            icon_from_db = self._icon_database[attr]
            len_icon_db = len(icon_from_db)
            if len_icon_db < 3:
                data, filetype = icon_from_db
                try:
                    return self._qpixmap_cache[data]
                except:
                    icon = QtGui.QPixmap.fromImage(
                        QtGui.QImage().fromData(QtCore.QByteArray.fromBase64(bytes(data, encoding='utf-8')),
                                                format=filetype))
                    self._qpixmap_cache[data] = icon
            else:
                data, filetype, data2 = icon_from_db
                try:
                    return self._qpixmap_cache[data]
                except:
                    icon = QtGui.QPixmap.fromImage(
                        QtGui.QImage().fromData(QtCore.QByteArray.fromBase64(bytes(data, encoding='utf-8')),
                                                format=filetype))
                    self._qpixmap_cache[data] = icon

            return icon
        return None


class Default3IconHandler(IconHandler):
    def __init__(self):
        super(Default3IconHandler, self).__init__()
        self._icon_database = image_dict3

    def __show_context(self):
        self.about1 = None
        self.accept_database2 = None
        self.address_book7 = None
        self.add_column4 = None
        self.add_database5 = None
        self.add_image6 = None
        self.add_row3 = None
        self.advance8 = None
        self.advertising9 = None
        self.alarm_clock14 = None
        self.alphabetical_sorting_az10 = None
        self.alphabetical_sorting_za11 = None
        self.answers12 = None
        self.approval13 = None
        self.approve15 = None
        self.area_chart16 = None
        self.assistant17 = None
        self.automatic19 = None
        self.bad_decision21 = None
        self.bar_chart18 = None
        self.bearish20 = None
        self.binoculars0 = None
        self.binoculars23 = None
        self.biohazard25 = None
        self.biomass22 = None
        self.biotech24 = None
        self.bookmark27 = None
        self.briefcase26 = None
        self.broken_link30 = None
        self.bullish28 = None
        self.business31 = None
        self.businessman33 = None
        self.businesswoman32 = None
        self.business_contact29 = None
        self.butting_in35 = None
        self.cable_release34 = None
        self.calculator36 = None
        self.calendar37 = None
        self.callback39 = None
        self.call_transfer38 = None
        self.camcorder41 = None
        self.camcorder_pro40 = None
        self.camera44 = None
        self.camera_addon42 = None
        self.camera_identification45 = None
        self.cancel43 = None
        self.candle_sticks46 = None
        self.capacitor47 = None
        self.cell_phone50 = None
        self.charge_battery49 = None
        self.checkmark48 = None
        self.circuit51 = None
        self.clapperboard52 = None
        self.clear_filters53 = None
        self.clock54 = None
        self.close_up_mode55 = None
        self.cloth63 = None
        self.collaboration57 = None
        self.collapse56 = None
        self.collect58 = None
        self.combo_chart59 = None
        self.comments60 = None
        self.compact_camera61 = None
        self.conference_call62 = None
        self.contacts65 = None
        self.copyleft64 = None
        self.copyright66 = None
        self.crystal_oscillator69 = None
        self.currency_exchange67 = None
        self.cursor68 = None
        self.customer_support70 = None
        self.dam71 = None
        self.database77 = None
        self.data_backup72 = None
        self.data_configuration74 = None
        self.data_encryption76 = None
        self.data_protection73 = None
        self.data_recovery75 = None
        self.data_sheet81 = None
        self.debt80 = None
        self.decision78 = None
        self.delete_column79 = None
        self.delete_database82 = None
        self.delete_row86 = None
        self.department84 = None
        self.deployment83 = None
        self.diploma_187 = None
        self.diploma_285 = None
        self.disapprove88 = None
        self.disclaimer95 = None
        self.dislike89 = None
        self.display90 = None
        self.document94 = None
        self.donate100 = None
        self.doughnut_chart97 = None
        self.down101 = None
        self.download99 = None
        self.down_left98 = None
        self.down_right96 = None
        self.do_not_inhale91 = None
        self.do_not_insert92 = None
        self.do_not_mix93 = None
        self.edit_image102 = None
        self.electrical_sensor103 = None
        self.electricity104 = None
        self.electronics106 = None
        self.electro_devices105 = None
        self.empty_battery107 = None
        self.empty_filter108 = None
        self.empty_trash109 = None
        self.end_call110 = None
        self.engineering111 = None
        self.entering_heaven_alive113 = None
        self.expand112 = None
        self.expired116 = None
        self.export114 = None
        self.external115 = None
        self.factory118 = None
        self.factory_breakdown117 = None
        self.faq119 = None
        self.feedback126 = None
        self.feed_in120 = None
        self.file121 = None
        self.filing_cabinet124 = None
        self.filled_filter122 = None
        self.film123 = None
        self.film_reel125 = None
        self.fine_print127 = None
        self.flash_auto128 = None
        self.flash_off130 = None
        self.flash_on129 = None
        self.flight307 = None
        self.flow_chart131 = None
        self.folder132 = None
        self.frame133 = None
        self.full_battery134 = None
        self.full_trash136 = None
        self.gallery135 = None
        self.genealogy138 = None
        self.generic_sorting_asc139 = None
        self.generic_sorting_desc137 = None
        self.globe140 = None
        self.good_decision142 = None
        self.graduation_cap141 = None
        self.grid144 = None
        self.headset143 = None
        self.heat_map145 = None
        self.high_battery146 = None
        self.high_priority147 = None
        self.home148 = None
        self.icons8_cup152 = None
        self.idea149 = None
        self.image_file150 = None
        self.import151 = None
        self.info154 = None
        self.inspection155 = None
        self.integrated_webcam156 = None
        self.internal159 = None
        self.invite157 = None
        self.in_transit153 = None
        self.ipad158 = None
        self.iphone160 = None
        self.key163 = None
        self.kindle161 = None
        self.landscape162 = None
        self.leave166 = None
        self.left169 = None
        self.left_down165 = None
        self.left_down2164 = None
        self.left_up167 = None
        self.left_up2168 = None
        self.library172 = None
        self.light_at_the_end_of_tunnel170 = None
        self.like173 = None
        self.like_placeholder171 = None
        self.line_chart176 = None
        self.link174 = None
        self.list178 = None
        self.lock179 = None
        self.lock_landscape175 = None
        self.lock_portrait177 = None
        self.low_battery180 = None
        self.low_priority181 = None
        self.make_decision183 = None
        self.manager184 = None
        self.medium_priority182 = None
        self.menu185 = None
        self.middle_battery186 = None
        self.mind_map188 = None
        self.minus187 = None
        self.missed_call189 = None
        self.mms191 = None
        self.money_transfer190 = None
        self.multiple_cameras192 = None
        self.multiple_devices193 = None
        self.multiple_inputs194 = None
        self.multiple_smartphones195 = None
        self.music196 = None
        self.negative_dynamic197 = None
        self.neutral_decision198 = None
        self.neutral_trading199 = None
        self.news200 = None
        self.next201 = None
        self.night_landscape202 = None
        self.night_portrait204 = None
        self.no_idea203 = None
        self.numerical_sorting_12205 = None
        self.numerical_sorting_21207 = None
        self.ok206 = None
        self.old_time_camera209 = None
        self.online_support210 = None
        self.opened_folder208 = None
        self.organization212 = None
        self.org_unit211 = None
        self.overtime217 = None
        self.package213 = None
        self.paid214 = None
        self.panorama216 = None
        self.parallel_tasks215 = None
        self.phone219 = None
        self.phone_android218 = None
        self.photo_reel220 = None
        self.picture226 = None
        self.pie_chart221 = None
        self.planner224 = None
        self.plus222 = None
        self.podium_without_speaker227 = None
        self.podium_with_audience223 = None
        self.podium_with_speaker225 = None
        self.portrait_mode231 = None
        self.positive_dynamic229 = None
        self.previous228 = None
        self.print232 = None
        self.privacy230 = None
        self.process233 = None
        self.puzzle234 = None
        self.questions235 = None
        self.radar_plot237 = None
        self.rating236 = None
        self.ratings238 = None
        self.reading240 = None
        self.reading_ebook243 = None
        self.redo239 = None
        self.refresh242 = None
        self.registered_trademark241 = None
        self.remove_image244 = None
        self.reuse248 = None
        self.right250 = None
        self.right_down246 = None
        self.right_down2245 = None
        self.right_up247 = None
        self.right_up2249 = None
        self.rotate_camera254 = None
        self.rotate_to_landscape251 = None
        self.rotate_to_portrait252 = None
        self.ruler255 = None
        self.rules253 = None
        self.safe256 = None
        self.sales_performance268 = None
        self.scatter_plot257 = None
        self.search258 = None
        self.selfie262 = None
        self.self_service_kiosk260 = None
        self.serial_tasks259 = None
        self.services263 = None
        self.service_mark261 = None
        self.settings264 = None
        self.share265 = None
        self.shipped266 = None
        self.shop271 = None
        self.signature267 = None
        self.sim_card270 = None
        self.sim_card_chip269 = None
        self.slr_back_side274 = None
        self.smartphone_tablet273 = None
        self.sms272 = None
        self.sound_recording_copyright275 = None
        self.speaker276 = None
        self.sports_mode277 = None
        self.stack_of_photos282 = None
        self.start278 = None
        self.statistics280 = None
        self.support281 = None
        self.survey283 = None
        self.switch_camera279 = None
        self.synchronize284 = None
        self.tablet_android285 = None
        self.template286 = None
        self.timeline289 = None
        self.todo_list287 = None
        self.trademark288 = None
        self.tree_structure290 = None
        self.two_smartphones292 = None
        self.undo291 = None
        self.unlock293 = None
        self.up296 = None
        self.upload297 = None
        self.up_left294 = None
        self.up_right295 = None
        self.video_call298 = None
        self.video_file299 = None
        self.video_projector304 = None
        self.view_details300 = None
        self.vip301 = None
        self.voicemail303 = None
        self.voice_presentation302 = None
        self.webcam305 = None
        self.workflow306 = None


class Default1IconHandler(IconHandler):
    def __init__(self):
        super(Default1IconHandler, self).__init__()
        self._icon_database = image_dict1

    def __show_context(self):
        """函数没有啥用处，只是为了能够提示补全"""
        self.dataOCR239 = None
        self.audio231 = None
        self.card238 = None
        self.clearData236 = None
        self.CompressionFile216 = None
        self.copyfile225 = None
        self.copyRename224 = None
        self.CoveredData235 = None
        self.engine223 = None
        self.excel232 = None
        self.findfolder212 = None
        self.findProcess220 = None
        self.hasFile210 = None
        self.hasfolder211 = None
        self.httpdownload219 = None
        self.httpUpload218 = None
        self.image226 = None
        self.lightcomponentall33 = None
        self.lightcomponentautomationclick132 = None
        self.lightcomponentautomationclipimage130 = None
        self.lightcomponentautomationdataCollection147 = None
        self.lightcomponentautomationdrag139 = None
        self.lightcomponentautomationgettarget131 = None
        self.lightcomponentautomationgettext137 = None
        self.lightcomponentautomationhighLight138 = None
        self.lightcomponentautomationradio133 = None
        self.lightcomponentautomationselectItem135 = None
        self.lightcomponentautomationTargetoptions143 = None
        self.lightcomponentautomationTargetsetting136 = None
        self.lightcomponentautomationTargetverify145 = None
        self.lightcomponentautomationtextinput140 = None
        self.lightcomponentautomationuiaotumation134 = None
        self.lightcomponentautomationwindowscard148 = None
        self.lightcomponentautomationwindowscard2141 = None
        self.lightcomponentbasestoprun188 = None
        self.lightcomponentcontrolCreatedata1 = None
        self.lightcomponentcontroldebugprint6 = None
        self.lightcomponentcontroldefaultCondition46 = None
        self.lightcomponentcontroldoublecondition4 = None
        self.lightcomponentcontroldowhile2 = None
        self.lightcomponentcontrolexitloop5 = None
        self.lightcomponentcontrolforeachlist3 = None
        self.lightcomponentcontrolforeachtimes0 = None
        self.lightcomponentcontrolif10 = None
        self.lightcomponentcontroliffalse11 = None
        self.lightcomponentcontroliftrue8 = None
        self.lightcomponentcontrolmanycondition13 = None
        self.lightcomponentcontrolnextloop7 = None
        self.lightcomponentcontrolsubflow9 = None
        self.lightcomponentcontroltrycatch192 = None
        self.lightcomponentcontrolwaiting12 = None
        self.lightcomponentcontrolwhile14 = None
        self.lightcomponentdataconvertcharacterreplace87 = None
        self.lightcomponentdataconvertcharactertimes85 = None
        self.lightcomponentdataconvertcharactertransform88 = None
        self.lightcomponentdataconvertclearcharacter86 = None
        self.lightcomponentdataconvertclearspace90 = None
        self.lightcomponentdataconvertcliptext84 = None
        self.lightcomponentdataconvertconvertText118 = None
        self.lightcomponentdataconvertdeletcharacter89 = None
        self.lightcomponentdataconvertfirstlocation92 = None
        self.lightcomponentdataconvertlistconverttotext91 = None
        self.lightcomponentdataconverttextconvertDatatime119 = None
        self.lightcomponentdataconverttextconvertnumber83 = None
        self.lightcomponentdataconverttextconverttolist94 = None
        self.lightcomponentdataconverttextnumber93 = None
        self.lightcomponentdataTextconvertjson157 = None
        self.lightcomponentdataTextconvertlist162 = None
        self.lightcomponentdatatimedatatime106 = None
        self.lightcomponentdatatimedifftime110 = None
        self.lightcomponentdatatimegetdatatime107 = None
        self.lightcomponentdatatimeturntime108 = None
        self.lightcomponentdatatimeturntimestamp109 = None
        self.lightcomponentDTclearDT70 = None
        self.lightcomponentDTcreateDT71 = None
        self.lightcomponentDTdeletrowcolum68 = None
        self.lightcomponentDTextractrowcolum69 = None
        self.lightcomponentDTforeachRow152 = None
        self.lightcomponentDTinsertrowcolum64 = None
        self.lightcomponentDTreverseDT65 = None
        self.lightcomponentDTrowcolum66 = None
        self.lightcomponentDTsortDT67 = None
        self.lightcomponentEncryptionfilehash198 = None
        self.lightcomponentEncryptionfilehashkey195 = None
        self.lightcomponentEncryptiontexthash197 = None
        self.lightcomponentEncryptiontexthashkey196 = None
        self.lightcomponentExcelareafill160 = None
        self.lightcomponentExcelcolumdeal19 = None
        self.lightcomponentExcelColumnfilter158 = None
        self.lightcomponentExcelColumnsort166 = None
        self.lightcomponentExcelcopyPaste16 = None
        self.lightcomponentExcelexit129 = None
        self.lightcomponentExcelfilter159 = None
        self.lightcomponentExcelMacro199 = None
        self.lightcomponentExcelnewrow163 = None
        self.lightcomponentExcelnewtable20 = None
        self.lightcomponentExcelopenfile17 = None
        self.lightcomponentExcelreadfile15 = None
        self.lightcomponentExcelrowdeal23 = None
        self.lightcomponentExcelrowforeach18 = None
        self.lightcomponentExceltabledeal21 = None
        self.lightcomponentExceltableforeach168 = None
        self.lightcomponentExcelwrite22 = None
        self.lightcomponentfiledealcopyfile47 = None
        self.lightcomponentfiledealcopyFolder50 = None
        self.lightcomponentfiledealdeleteFile58 = None
        self.lightcomponentfiledealdeleteFolder61 = None
        self.lightcomponentfiledealfileRename48 = None
        self.lightcomponentfiledealfindfile249 = None
        self.lightcomponentfiledealfindfile29 = None
        self.lightcomponentfiledealfindfile62 = None
        self.lightcomponentfiledealfindfolder161 = None
        self.lightcomponentfiledealmovefile51 = None
        self.lightcomponentfiledealmoveFolder60 = None
        self.lightcomponentfiledealnewfile56 = None
        self.lightcomponentfiledealnewFolder57 = None
        self.lightcomponentfiledealreadcsv255 = None
        self.lightcomponentfiledealreadcsv32 = None
        self.lightcomponentfiledealreadcsv63 = None
        self.lightcomponentfiledealreadfilecontent53 = None
        self.lightcomponentfiledealreadtxt30 = None
        self.lightcomponentfiledealreadtxt59 = None
        self.lightcomponentfiledealrenameFolder54 = None
        self.lightcomponentfiledealwritecsv52 = None
        self.lightcomponentfiledealwritefilecontent72 = None
        self.lightcomponentimagedeal74 = None
        self.lightcomponentimagedealcompany77 = None
        self.lightcomponentimagedealdriver80 = None
        self.lightcomponentimagedealIdentification79 = None
        self.lightcomponentimagedealinvoice81 = None
        self.lightcomponentimagedealrealestate76 = None
        self.lightcomponentimagedealtable78 = None
        self.lightcomponentimagedealtext82 = None
        self.lightcomponentimagedealverificationIdentify171 = None
        self.lightcomponentkvK97 = None
        self.lightcomponentkvKdelete104 = None
        self.lightcomponentkvKsort100 = None
        self.lightcomponentkvKtoV98 = None
        self.lightcomponentkvKtoVupdata103 = None
        self.lightcomponentkvKV102 = None
        self.lightcomponentkvKV101 = None
        self.lightcomponentkvKVclear99 = None
        self.lightcomponentkvKVinsert105 = None
        self.lightcomponentlistdealclearlist124 = None
        self.lightcomponentlistdealcreatlist122 = None
        self.lightcomponentlistdealcreatlist95 = None
        self.lightcomponentlistdealdealelement120 = None
        self.lightcomponentlistdealdeleteelement125 = None
        self.lightcomponentlistdealelementamount127 = None
        self.lightcomponentlistdealinsertelement126 = None
        self.lightcomponentlistdealmergelist123 = None
        self.lightcomponentlistdealReverseelement121 = None
        self.lightcomponentlistdealSort128 = None
        self.lightcomponentmathabs116 = None
        self.lightcomponentmathfloor114 = None
        self.lightcomponentmathmod117 = None
        self.lightcomponentmathpower112 = None
        self.lightcomponentmathrandom113 = None
        self.lightcomponentmathROUND111 = None
        self.lightcomponentmathSQRT115 = None
        self.lightcomponentNLP75 = None
        self.lightcomponentNLPemotion73 = None
        self.lightcomponentNLPentity96 = None
        self.lightcomponentoutlookfindmail35 = None
        self.lightcomponentoutlookForwardmail31 = None
        self.lightcomponentoutlookmailannex36 = None
        self.lightcomponentoutlookmaildeal37 = None
        self.lightcomponentoutlookopenmail34 = None
        self.lightcomponentoutlookreadmail39 = None
        self.lightcomponentoutlooksendmail38 = None
        self.lightcomponentPDFconvertimage207 = None
        self.lightcomponentPDFimageamount200 = None
        self.lightcomponentPDFmerge201 = None
        self.lightcomponentPDFpage202 = None
        self.lightcomponentPDFreadtext203 = None
        self.lightcomponentPDFsaveimage205 = None
        self.lightcomponentPDFtableamount204 = None
        self.lightcomponentPDFtabledata206 = None
        self.lightcomponentprotocolhttp165 = None
        self.lightcomponentprotocolhttpdownload164 = None
        self.lightcomponentsystemmessagebox153 = None
        self.lightcomponentsystempromptmessagebox154 = None
        self.lightcomponentuiaactivewindow174 = None
        self.lightcomponentuiaactivityElement142 = None
        self.lightcomponentuiaclosewindow167 = None
        self.lightcomponentuiadropdownlist150 = None
        self.lightcomponentuiaedittext144 = None
        self.lightcomponentuiaelementAttributes194 = None
        self.lightcomponentuiafindelement155 = None
        self.lightcomponentuiafindimage193 = None
        self.lightcomponentuiafocus146 = None
        self.lightcomponentuiagetwindow169 = None
        self.lightcomponentuiahotkey151 = None
        self.lightcomponentuiahover149 = None
        self.lightcomponentuiainput2186 = None
        self.lightcomponentuiaKM187 = None
        self.lightcomponentuialocation176 = None
        self.lightcomponentuialocationClick175 = None
        self.lightcomponentuiamax173 = None
        self.lightcomponentuiamouseimage191 = None
        self.lightcomponentuiaScreenshot2172 = None
        self.lightcomponentuiaselection170 = None
        self.lightcomponentuiaverification156 = None
        self.lightcomponentuiawaitelement190 = None
        self.lightcomponentuiawaitimage189 = None
        self.lightcomponentuiautomationclickelement24 = None
        self.lightcomponentuiautomationdataCollection45 = None
        self.lightcomponentuiautomationgettext25 = None
        self.lightcomponentuiautomationTargetoptions40 = None
        self.lightcomponentuiautomationTargetsetting41 = None
        self.lightcomponentuiautomationTargetverify42 = None
        self.lightcomponentuiautomationtextinput26 = None
        self.lightcomponentuiautomationwindowscard28 = None
        self.lightcomponentuiautomationwindowscard227 = None
        self.lightcomponentwordexit184 = None
        self.lightcomponentwordfindCopy178 = None
        self.lightcomponentwordfindlocation185 = None
        self.lightcomponentwordmark179 = None
        self.lightcomponentwordmarklocation181 = None
        self.lightcomponentwordopen180 = None
        self.lightcomponentwordreadtext182 = None
        self.lightcomponentwordtype183 = None
        self.lightrightbarlogpanelaction43 = None
        self.lightrightbarlogpanelsubflow44 = None
        self.pdf230 = None
        self.pythonscrip208 = None
        self.readData237 = None
        self.ruler177 = None
        self.runcube209 = None
        self.SMTP215 = None
        self.stopProcess221 = None
        self.style214 = None
        self.txt229 = None
        self.unkonw227 = None
        self.unlocklock213 = None
        self.Unzip217 = None
        self.verificationIdentify222 = None
        self.video233 = None
        self.word228 = None
        self.zip234 = None


class DefaultIconHandler(IconHandler):
    def __init__(self):
        super(DefaultIconHandler, self).__init__()
        self._icon_database = image_dict

    def __show_context(self):
        """函数没有啥用处，只是为了能够提示补全"""
        self.ACos563 = None
        self.ACot561 = None
        self.ARanalysis598 = None
        self.ASin569 = None
        self.ATan562 = None
        self.Absolutecenter432 = None
        self.Absoluteisometric425 = None
        self.Absolutevalue564 = None
        self.Accelerate367 = None
        self.Accountnumber196 = None
        self.Accountnumber740 = None
        self.Add592 = None
        self.Adddata231 = None
        self.Adddata6 = None
        self.Addfigure657 = None
        self.Addframecheme31 = None
        self.Addlayer29 = None
        self.Addline344 = None
        self.Addplottingmap88 = None
        self.Addressmatch817 = None
        self.Advancedfeatures22 = None
        self.Advancedtools35 = None
        self.Aggregate802 = None
        self.Aggregationdiagram251 = None
        self.Aggregationfigure754 = None
        self.Aimingpointalignment266 = None
        self.Airqualityanalysis606 = None
        self.Align694 = None
        self.Alignends265 = None
        self.Alignleft272 = None
        self.Alignleft421 = None
        self.Alignright279 = None
        self.Alignright407 = None
        self.Alignup413 = None
        self.Amendment258 = None
        self.Analysis773 = None
        self.Analysismode139 = None
        self.Analysisprocess517 = None
        self.And627 = None  # asdf
        self.Annotationmanagement239 = None
        self.Area310 = None
        self.Areadrawing796 = None
        self.Armap107 = None
        self.Artificialneuralnetworkcellularautomata816 = None
        self.Artificialneuralnetworktraining809 = None
        self.Ascending340 = None
        self.Associatedbrowsing191 = None
        self.Attribute343 = None
        self.Attributeextraction166 = None
        self.Attributetodictionary583 = None
        self.Automaticcrolling73 = None
        self.Autumn599 = None
        self.Auxiliarydrawing41 = None
        self.Avoidaddingpictures87 = None
        self.Avoidancearea485 = None
        self.Avoidancearea778 = None
        self.Avoiddeletingpictures482 = None
        self.Avoiddeletingpictures80 = None
        self.BIMlightweight441 = None
        self.Backgroundcolor267 = None
        self.Bandmanagement656 = None
        self.Batchdrawing621 = None
        self.Batchgenerationcache164 = None
        self.Blackandwhite618 = None
        self.Blank244 = None
        self.Blocktatistics803 = None
        self.Blocktatistics825 = None
        self.Bold280 = None
        self.Booleanoperation451 = None
        self.Bottom405 = None
        self.Box371 = None
        self.Bright538 = None
        self.Brightness584 = None
        self.Browse771 = None
        self.Browsecene750 = None
        self.Browsemaps752 = None
        self.Browsemode594 = None
        self.Browseproperties718 = None
        self.Bshapeampling544 = None
        self.Buffer157 = None
        self.Buildinganetwork155 = None
        self.Buildinghouses513 = None
        self.Buildingpitchedroofs438 = None
        self.Buildnetwork726 = None
        self.Buildtim168 = None
        self.By596 = None
        self.CMYKmode566 = None
        self.Cache325 = None
        self.Calculategeometricattributes335 = None
        self.Calculatehortestpath_grid_671 = None
        self.Calculatethehortestpath_vector_672 = None
        self.Calculatethehortestpath675 = None
        self.Cancel214 = None
        self.Cartography127 = None
        self.Centeralignment273 = None
        self.Centerleftandright420 = None
        self.Centerupanddown430 = None
        self.Chart114 = None
        self.Chartdatawarehousing20 = None
        self.Check217 = None
        self.Classdiagram652 = None
        self.Clear221 = None
        self.Clear293 = None
        self.Clicktart50 = None
        self.Closeall192 = None
        self.Closedocument17 = None
        self.Clusterdistribution138 = None
        self.Color286 = None
        self.Color595 = None
        self.Coloradjustment712 = None
        self.Colorchannel567 = None
        self.Colorcheme831 = None
        self.Colorenhancement586 = None
        self.Colorlibrary625 = None
        self.Colormanagement777 = None
        self.Columnartackingfigure785 = None
        self.Combination416 = None
        self.Combination691 = None
        self.Compass427 = None
        self.Compoundtyle241 = None
        self.Compressandmonomer180 = None
        self.Computer3 = None
        self.Condition620 = None
        self.Cone376 = None
        self.Connectedtochart808 = None
        self.Connectedtochartot812 = None
        self.Connection216 = None
        self.Constructvoxelgrid165 = None
        self.Contour276 = None
        self.Contour408 = None
        self.Contour805 = None
        self.Contouranalysis471 = None
        self.Contrast585 = None
        self.Controlpointetting715 = None
        self.Convertfromline360 = None
        self.Convertfromlinetopath369 = None
        self.Convertfromlinetotation363 = None
        self.Convertymbollibrary659 = None
        self.Convexhull445 = None
        self.Cooltone645 = None
        self.Coordinatepositioning11 = None
        self.Copy292 = None
        self.Copy45 = None
        self.Cos582 = None
        self.Cosh588 = None
        self.Createaddressindex649 = None
        self.Createampleclassificationtemplate632 = None
        self.Createmapindex648 = None
        self.Createrandompoints814 = None
        self.Createroofelevationinformation572 = None
        self.Curvepath98 = None
        self.Custom201 = None
        self.Custom257 = None
        self.Custom653 = None
        self.Custom764 = None
        self.Custom801 = None
        self.Customlegend650 = None
        self.Custompanel504 = None
        self.Customtemplatemanagement798 = None
        self.Cylinder381 = None
        self.DEMbuild148 = None
        self.Data736 = None
        self.Dataacquisition116 = None
        self.Database117 = None
        self.Databasetype110 = None
        self.Dataconsolidation60 = None
        self.Datadownload206 = None
        self.Dataexport122 = None
        self.Dataharing173 = None
        self.Dataharing521 = None
        self.Dataimport123 = None
        self.Datamanagement175 = None
        self.Dataource744 = None
        self.Dataource829 = None
        self.Dataourceconversion529 = None
        self.Dataourceconversion727 = None
        self.Dataplitting59 = None
        self.Dataprocessing178 = None
        self.Dataprocessing757 = None
        self.Dataprocessing762 = None
        self.Dataprocessing9 = None
        self.Datasetprojectionconversion0 = None
        self.Datatorageconversion530 = None
        self.Dataupdate1 = None
        self.Dataupload204 = None
        self.Datawarehousing77 = None
        self.Decelerate364 = None
        self.Defaultattribute33 = None
        self.Defaultattribute483 = None
        self.Delayedrefresh27 = None
        self.Deleteduplicatepoints557 = None
        self.Deleteline283 = None
        self.Deleteline341 = None
        self.Deleteuspendedolids440 = None
        self.Densityanalysis137 = None
        self.Densityclustering532 = None
        self.Descending338 = None
        self.Desktop67 = None
        self.Dictionarylibrary624 = None
        self.Dictionarylibraryfile647 = None
        self.Dictionarytoattribute611 = None
        self.Digging448 = None
        self.Disassembling423 = None
        self.Display44 = None
        self.Displayactionlabel48 = None
        self.Displayallrecords515 = None
        self.Displaymode39 = None
        self.Displaynavigationchart66 = None
        self.Displaytheelectedrecord520 = None
        self.Displaytime615 = None
        self.Distance311 = None
        self.Distance748 = None
        self.Distancegrid145 = None
        self.Dmplusworkspace679 = None
        self.Document113 = None
        self.Dotchart791 = None
        self.Drawing781 = None
        self.Drawingettings297 = None
        self.Drawinginspection21 = None
        self.Drawlocator644 = None
        self.Dynamicegmentation161 = None
        self.Dynamicegmentation731 = None
        self.Dynamictext612 = None
        self.EGCelevationtorage38 = None
        self.EPSexport635 = None
        self.EPSimport590 = None
        self.Eagleeye224 = None
        self.Edit706 = None
        self.Ellipsoid379 = None
        self.Environmentettings143 = None
        self.Equalize419 = None
        self.Equalize821 = None
        self.Equalto629 = None
        self.Equalwidth433 = None
        self.Equalwidth804 = None
        self.Escrow667 = None
        self.Except610 = None
        self.Execute751 = None
        self.Execution215 = None
        self.ExitHide65 = None
        self.ExitZoom92 = None
        self.Exitretreat84 = None
        self.Export213 = None
        self.Exportamplelibrary637 = None
        self.Exportastool209 = None
        self.Exportquicklaunch502 = None
        self.Exporttatisticalchart242 = None
        self.Exporttopython210 = None
        self.Extract3Ddata182 = None
        self.Extractattribute167 = None
        self.Extractboundaryline129 = None
        self.Extractdata187 = None
        self.Extractdata512 = None
        self.Extractmvalue162 = None
        self.FTPdirectory810 = None
        self.Face299 = None
        self.Face409 = None
        self.Fenceanalysis536 = None
        self.Fieldindex104 = None
        self.Figure501 = None
        self.Fileelection172 = None
        self.Filetype118 = None
        self.Fillandcutanalysis474 = None
        self.Filltyle725 = None
        self.Fillymbol282 = None
        self.Fillymbol355 = None
        self.Fillymbol404 = None
        self.Findandlocate233 = None
        self.Fixedize271 = None
        self.Flashing8 = None
        self.Flight10 = None
        self.Flight365 = None
        self.Flowpatterncorrection524 = None
        self.Folder826 = None
        self.Forecast551 = None
        self.Foregroundcolor268 = None
        self.Forward666 = None
        self.Fourcolors261 = None
        self.Frontview76 = None
        self.Fullcreen90 = None
        self.Fullcreenpreview495 = None
        self.Fullpagedisplay396 = None
        self.Fullwidth225 = None
        self.Fullwidth399 = None
        self.Fullwidth475 = None
        self.Functionbutton516 = None
        self.Fusion2 = None
        self.GDBimport638 = None
        self.Generate2D463 = None
        self.Generatedistancegrid674 = None
        self.Generatedistancegrid677 = None
        self.Generatedom468 = None
        self.Generatedsm469 = None
        self.Generateelevation462 = None
        self.Generatemapcacheandpublish665 = None
        self.Generatemapcheme32 = None
        self.Generatemodelcacheandpublish660 = None
        self.Generatepatialweightmatrixfile134 = None
        self.Generatepointcloudcache183 = None
        self.Generatepointcloudcacheandpublish668 = None
        self.Generatetincacheandpublish662 = None
        self.Generateviewframelist36 = None
        self.Geographicimulation811 = None
        self.Geologicalbody184 = None
        self.Global324 = None
        self.Global86 = None
        self.Globalcoherentroaming63 = None
        self.Gotothelastline332 = None
        self.Grademovementymbol250 = None
        self.Gradeymbol255 = None
        self.Gradeymbol772 = None
        self.Grayscale600 = None
        self.Greaterthan609 = None
        self.Greaterthanorequalto581 = None
        self.Grid806 = None
        self.Gridanalysis737 = None
        self.Griddiagram245 = None
        self.Gridquery141 = None
        self.Gridtatistics152 = None
        self.Gridvectorization720 = None
        self.GroundtreetView658 = None
        self.Growth99 = None
        self.HSBmode568 = None
        self.Harddisk93 = None
        self.Height318 = None
        self.Help776 = None
        self.Hex337 = None
        self.Hidecolumn345 = None
        self.Hiderow342 = None
        self.Hideystemfield329 = None
        self.Histogram142 = None
        self.Histogram789 = None
        self.Horizontalcenter411 = None
        self.Horizontalequidistant431 = None
        self.Horizontaltext499 = None
        self.Hue579 = None
        self.Hydrologicalanalysis146 = None
        self.Iconfile356 = None
        self.Image_Normal177 = None
        self.Imagedataconversion46 = None
        self.Imagedatawarehousing69 = None
        self.Imagepyramid124 = None
        self.Imagethematiccut68 = None
        self.Implementation156 = None
        self.Import208 = None
        self.Importamplelibrary628 = None
        self.Importcogo522 = None
        self.Importdrawinginformation603 = None
        self.Importingplacenameinformation54 = None
        self.Importtocurrentwindow211 = None
        self.Inclinedtorage170 = None
        self.Inclinedtorage465 = None
        self.Informationboard503 = None
        self.Informationinquiry75 = None
        self.Interpolationanalysis140 = None
        self.Intervisibilityanalysis466 = None
        self.Inundationanalysis472 = None
        self.Invisible323 = None
        self.Issue489 = None
        self.Italic275 = None
        self.Iterationfile815 = None
        self.Iterativedataset818 = None
        self.Key414 = None
        self.Key78 = None
        self.Labelmode190 = None
        self.Labelpretreatment263 = None
        self.Ladderdiagram790 = None
        self.Landmark383 = None
        self.Largecreenproduction497 = None
        self.Layercontrol34 = None
        self.Layerplayback605 = None
        self.Layerproperties230 = None
        self.Layerproperties309 = None
        self.Layertyle284 = None
        self.Layertyle743 = None
        self.Layout121 = None
        self.Layoutbrowsing700 = None
        self.Layoutettings697 = None
        self.Layoutproperties390 = None
        self.Layoutproperties714 = None
        self.LeftItalic277 = None
        self.Lessthan639 = None
        self.Licenseplaterecognition542 = None
        self.Line302 = None
        self.Line417 = None
        self.Lineardistancegrid678 = None
        self.Linechart794 = None
        self.Linetopologycheck130 = None
        self.Linetyle747 = None
        self.Linetylecolor288 = None
        self.Lineymbol281 = None
        self.Lineymbol357 = None
        self.Lineymbol403 = None
        self.Loadingtatistics256 = None
        self.Loadmapcheme26 = None
        self.Localtiles203 = None
        self.Localupdate96 = None
        self.Localvideo491 = None
        self.Lockmap392 = None
        self.Longitudinallycentered422 = None
        self.Loweralignment424 = None
        self.MDBimport651 = None
        self.MXDtoxwu661 = None
        self.Magnifyingglass223 = None
        self.Management205 = None
        self.Management763 = None
        self.Map111 = None
        self.Map415 = None
        self.Mapclipping234 = None
        self.Mapcollaboration767 = None
        self.Mapediting721 = None
        self.Mapettings354 = None
        self.Maphutter765 = None
        self.Mapmeasurement227 = None
        self.Mapoperations709 = None
        self.Mappositioning61 = None
        self.Mapproperties229 = None
        self.Mapreset23 = None
        self.Maproaming386 = None
        self.Maprollerhutter236 = None
        self.Margins394 = None
        self.Matrixtyle240 = None
        self.Measuringgeographicaldistribution136 = None
        self.Mergetinprofiles510 = None
        self.Migrationettings655 = None
        self.Militarydatawarehousing24 = None
        self.Militarymappluginregistration4 = None
        self.Militarymappluginuninstall12 = None
        self.Minus565 = None
        self.Mode597 = None
        self.Model775 = None
        self.Modeldrawing688 = None
        self.Modelediting455 = None
        self.Modelflattening188 = None
        self.Modeloperation701 = None
        self.Modelprocessing174 = None
        self.Modifynovalue823 = None
        self.Modulus630 = None
        self.Mongdbtile232 = None
        self.Mongotile200 = None
        self.Mongoworkspace683 = None
        self.Movedownonelayer406 = None
        self.Moveuponelayer412 = None
        self.MySQLworkspace680 = None
        self.Mydocuments25 = None
        self.Navalchartdatawarehousing71 = None
        self.Navigatetothefirstline328 = None
        self.NetCDF613 = None
        self.Networkanalysis151 = None
        self.New218 = None
        self.New362 = None
        self.Newbulletinboard370 = None
        self.Newdataset738 = None
        self.NewdesktopUIcolorchanges193 = None
        self.Newfolder202 = None
        self.Newtatisticalchart708 = None
        self.Noanimation18 = None
        self.Non578 = None
        self.NonGJBdatawarehousing70 = None
        self.Normal189 = None
        self.Notequalto575 = None
        self.Numberofinglevalues = None
        self.Objectdrawing580 = None
        self.Objectdrawing755 = None
        self.Objectediting716 = None
        self.Objectoperation704 = None
        self.Objectorder693 = None
        self.Objecttyle287 = None
        self.Obliqueclipping437 = None
        self.Obliqueinlay454 = None
        self.Onlinemap197 = None
        self.Onlinemap321 = None
        self.Onlinemap832 = None
        self.Onlinevideo500 = None
        self.Onlineymbol830 = None
        self.Open361 = None
        self.Opendocument16 = None
        self.Openinganalysis464 = None
        self.Openituationchart13 = None
        self.Openplottingmap49 = None
        self.Operation479 = None
        self.Operation703 = None
        self.Operation746 = None
        self.Or570 = None
        self.Oracleplusworkspace685 = None
        self.Ordinaryleastquares548 = None
        self.Originalinformationmanagement643 = None
        self.Orthogonalpolygon304 = None
        self.Orthogonalrightanglediagram593 = None
        self.Outputandprinting705 = None
        self.Outputpdf14 = None
        self.Outputpdf395 = None
        self.Outputpicture391 = None
        self.Outputpicture58 = None
        self.Pageetup717 = None
        self.Paperdirection397 = None
        self.Paperize401 = None
        self.Paste294 = None
        self.Paste83 = None
        self.Picture393 = None
        self.Picture498 = None
        self.Piechart786 = None
        self.Pipelineflow663 = None
        self.Placenameinquiry95 = None
        self.Play40afterthepreviousaction = None
        self.Plotlayercontroller51 = None
        self.Plotpanel759 = None
        self.Point295 = None
        self.Point429 = None
        self.PointCloudToList176 = None
        self.PointCloudToOSGB186 = None
        self.Pointadjustment807 = None
        self.Pointcloud770 = None
        self.Pointdensity247 = None
        self.Pointdensity732 = None
        self.Pointmatchlinedirection = None
        self.Pointtyle782 = None
        self.Pointymbol274 = None
        self.Pointymbol353 = None
        self.Pointymbol402 = None
        self.Polygon820 = None
        self.Polygonelection313 = None
        self.Polylinepath97 = None
        self.Polymerization824 = None
        self.Positioning339 = None
        self.Positioning5 = None
        self.PostGISworkspace684 = None
        self.PostgreSQLworkspace682 = None
        self.Previewpicture94 = None
        self.Prickedit480 = None
        self.Prickpoint477 = None
        self.Principalcomponentanalysiscellularautomata819 = None
        self.Principalcomponentanalysistraining822 = None
        self.Printmapbook604 = None
        self.Printpreview388 = None
        self.Profile181 = None
        self.Projectionconversion120 = None
        self.Projectionettings112 = None
        self.Property749 = None
        self.Propertyheet108 = None
        self.Propertyheet53 = None
        self.Proximityanalysis150 = None
        self.Publishindex617 = None
        self.Publishiservice742 = None
        self.Pulldownfunctionbutton511 = None
        self.Pyramid377 = None
        self.Python119 = None
        self.Query780 = None
        self.Querycoordinatevalue315 = None
        self.Querymvalue160 = None
        self.RGBmode616 = None
        self.Randomampling545 = None
        self.Rasterimage779 = None
        self.Realtimetreamingdata760 = None
        self.Rearview74 = None
        self.Recoverytask195 = None
        self.Redo290 = None
        self.Refresh308 = None
        self.Registration115 = None
        self.Registration476 = None
        self.Registrationbrowsing711 = None
        self.Registrationmode576 = None
        self.Remoteensingmapping126 = None
        self.Removeoption30 = None
        self.Resetdefaultproperty481 = None
        self.Resetpicture81 = None
        self.Restoredefaultparameterettings543 = None
        self.Resulttorage535 = None
        self.Reversecolor614 = None
        self.Revocation289 = None
        self.Ringdiagram793 = None
        self.Roadnetworkanalysis758 = None
        self.Roaming238 = None
        self.Roaming478 = None
        self.Rose787 = None
        self.Rotationangle269 = None
        self.Rounddown623 = None
        self.Rulemodeling710 = None
        self.SDBtoudb526 = None
        self.SDEimport669 = None
        self.SHPimport636 = None
        self.SQLquery159 = None
        self.SQLtatementquery813 = None
        self.Samplelabelextraction646 = None
        self.Samplemanagement631 = None
        self.Saturation601 = None
        self.Save103 = None
        self.Save359 = None
        self.Save57 = None
        self.Saveas358 = None
        self.SaveasExcel327 = None
        self.SaveasExcel641 = None
        self.Saveasdataset243 = None
        self.Saveasdataset333 = None
        self.Saveastool212 = None
        self.Savetotemplatelibrary799 = None
        self.Scale434 = None
        self.Scenario109 = None
        self.Sceneclipping320 = None
        self.Sceneproperties312 = None
        self.Scenerollerhutter322 = None
        self.Screening331 = None
        self.Screening514 = None
        self.Secondarydevelopmentexample537 = None
        self.Sectionanalysis460 = None
        self.Sectionandprojection446 = None
        self.See319 = None
        self.Select237 = None
        self.Select305 = None
        self.Selectpath72 = None
        self.Selectroaming306 = None
        self.Service207 = None
        self.Service784 = None
        self.Setgriddata91 = None
        self.Setting228 = None
        self.Setting626 = None
        self.Settingout449 = None
        self.Settings296 = None
        self.Shadowbody452 = None
        self.Shadows285 = None
        self.Sharpening591 = None
        self.Shear291 = None
        self.Shear62 = None
        self.Shrink226 = None
        self.Shrinkby400 = None
        self.Sin589 = None
        self.Singlepointareaestimation546 = None
        self.Singlevalue259 = None
        self.Singlevalue723 = None
        self.Singlevaluetyle260 = None
        self.Sitemanagement368 = None
        self.Situationdeduction56 = None
        self.Situationdeduction733 = None
        self.Size699 = None
        self.Sketch654 = None
        self.Skylineanalysis467 = None
        self.Slopeaspectanalysis473 = None
        self.Snapettings300 = None
        self.Snapettings410 = None
        self.Solarradiation147 = None
        self.Spatialindex106 = None
        self.Spatialquery158 = None
        self.Spatialquery435 = None
        self.Spatialrelationshipmodeling135 = None
        self.Spatialtatisticalanalysis686 = None
        self.Specialeffects607 = None
        self.Sphere378 = None
        self.Split633 = None
        self.Splitline490 = None
        self.Sqlplusworkspace681 = None
        self.Stackanalysis154 = None
        self.Standarddeviation347 = None
        self.Staticmodel372 = None
        self.Statisticalanalysis713 = None
        self.Statisticalchart105 = None
        self.Statisticalchart640 = None
        self.Statisticalchartconversion696 = None
        self.Statisticalchartprocessing698 = None
        self.Statisticalinference547 = None
        self.Statisticalmovementymbol253 = None
        self.Statistics252 = None
        self.Statistics730 = None
        self.Stop366 = None
        self.Stop37 = None
        self.Straw608 = None
        self.Streamingvideo496 = None
        self.Stretch456 = None
        self.Stretchettings728 = None
        self.Style769 = None
        self.Stylebrush79 = None
        self.Stylemigration719 = None
        self.Subection741 = None
        self.Subject774 = None
        self.Subparagraph262 = None
        self.Summaryfield330 = None
        self.Summer619 = None
        self.Sunshineanalysis461 = None
        self.Surfaceanalysis153 = None
        self.Suspension15 = None
        self.Switchunderlay43 = None
        self.Symbollibrary827 = None
        self.Systemmodewitching55 = None
        self.Tagmovetag246 = None
        self.Tan642 = None
        self.Targetdetection541 = None
        self.Targetdetectionettings534 = None
        self.Targettracking539 = None
        self.Targettrackingettings549 = None
        self.Taskmanagement199 = None
        self.Technicalupport219 = None
        self.Templatemanagement248 = None
        self.Templatemanagement800 = None
        self.Tensileclosure436 = None
        self.Terrainmodification444 = None
        self.Terrainmodificationmodel185 = None
        self.Text298 = None
        self.Text426 = None
        self.Textfind519 = None
        self.Texttemplate702 = None
        self.Texttyle687 = None
        self.Textureextraction459 = None
        self.Texturereplacement457 = None
        self.Theaveragevalueis349 = None
        self.Theettingratiois85 = None
        self.Thermodynamicdiagram254 = None
        self.Theurfacedistancefromthegridis670 = None
        self.ThreeDanalysis689 = None
        self.ThreeDbuffer443 = None
        self.ThreeDcircle374 = None
        self.ThreeDcolumnartackingfigure792 = None
        self.ThreeDface380 = None
        self.ThreeDfielddata768 = None
        self.ThreeDline385 = None
        self.ThreeDplottingattributes487 = None
        self.ThreeDplottingpanel488 = None
        self.ThreeDplottingpanel89 = None
        self.ThreeDplottingproperties102 = None
        self.ThreeDpoint384 = None
        self.ThreeDpolyline382 = None
        self.ThreeDrose788 = None
        self.Threedimensionalhistogram797 = None
        self.Threedimensionalpiechart795 = None
        self.Threedimensionalvolumeanalysis692 = None
        self.Tiltphotographingdataoperation695 = None
        self.Tiltphotography756 = None
        self.Tiltwarehousing525 = None
        self.TinBooleanbudget447 = None
        self.Tincutting453 = None
        self.Tindig450 = None
        self.Tininlay458 = None
        self.Tinterrain179 = None
        self.Tinterrain722 = None
        self.Tinterrainoperation690 = None
        self.Tool783 = None
        self.Toolbar82 = None
        self.Topologicalplane133 = None
        self.Topology724 = None
        self.Topologycheck132 = None
        self.Topologynetwork163 = None
        self.Topologynetwork735 = None
        self.Toponymicinformation47 = None
        self.Topping418 = None
        self.Total348 = None
        self.Track307 = None
        self.Trajectorymodel375 = None
        self.Transparentbackground270 = None
        self.Tree373 = None
        self.Treediagram622 = None
        self.Triangulationoperation442 = None
        self.TwoDplotattributes486 = None
        self.TwoDplottingattributes101 = None
        self.TwoDplottingpanel28 = None
        self.TwoDplottingpanel484 = None
        self.TwoDtopologypreprocessing128 = None
        self.Twopointhortesturfacepath673 = None
        self.Twopointminimumcostpath676 = None
        self.Typeconversion131 = None
        self.Typeconversion171 = None
        self.Typeconversion509 = None
        self.UDBtoudbx527 = None
        self.UIcolormatchingmodification194 = None
        self.Udbxtoudb528 = None
        self.Underground729 = None
        self.Undergroundcolor316 = None
        self.Underline278 = None
        self.Unhidecolumn336 = None
        self.Unhiderow334 = None
        self.Unifiedtyle249 = None
        self.Unifiedtyle739 = None
        self.Unit220 = None
        self.Unit314 = None
        self.Updatecolumn326 = None
        self.Upgradetolargefile508 = None
        self.Upto602 = None
        self.Utility144 = None
        self.Variance346 = None
        self.Vectoranalysis753 = None
        self.Vectorgridconversion149 = None
        self.Vectorizationline303 = None
        self.Vectorizationplane301 = None
        self.Velocityanalysis540 = None
        self.Verticallyequidistant428 = None
        self.Verticaltext494 = None
        self.Video533 = None
        self.Videodataset577 = None
        self.Videoparameters492 = None
        self.Videotag493 = None
        self.View64 = None
        self.View745 = None
        self.Viewableanalysis470 = None
        self.Viewelection531 = None
        self.Viewportmanagement734 = None
        self.Violationdetection587 = None
        self.Visualmodeling707 = None
        self.Voxelgridgenerationcache169 = None
        self.Warehousingandpublishing3Dervice664 = None
        self.Warmtone634 = None
        self.Web125 = None
        self.Window761 = None
        self.Workingdirectory52 = None
        self.Workspace198 = None
        self.Workspace766 = None
        self.Workspace828 = None
        self.XOR574 = None
        self.Zoom100 = None
        self.Zoom235 = None
        self.Zoomin222 = None
        self.Zoomin398 = None
        self.Zoominonthemap387 = None
        self.Zoomoutonthemap389 = None
        self.Zoomreferencepicture42 = None
        self.Zoomthemap19 = None
        self.ai571 = None
        self.bim439 = None
        self.bim507 = None
        self.cogo518 = None
        self.cot550 = None
        self.cotH558 = None
        self.dm7 = None
        self.exp556 = None
        self.kml317 = None
        self.ln553 = None
        self.log552 = None
        self.max352 = None
        self.min351 = None
        self.ndvi505 = None
        self.ndwi506 = None
        self.pow555 = None
        self.sinH560 = None
        self.sqrt554 = None
        self.tanH559 = None
        self.vectortext573 = None
        self.xugu523 = None
        self.default_logo = None
        self.A_Basin882 = None
        self.A_Dat_file_to_csv_file_848 = None
        self.A_Dat_file_to_csv_file_863 = None
        self.A_MAPX_to_sxwu845 = None
        self.A_MAPX_to_sxwu878 = None
        self.A_Watershed886 = None
        self.A_Face_coding_896 = None
        self.A_Volume_data_set_915 = None
        self.A_Distance_to_ground_833 = None
        self.A_According_to_the_area_of_835 = None
        self.A_Full_screen_858 = None
        self.A_Other_905 = None
        self.A_Create_line_rule_points_854 = None
        self.A_Create_polygon_rule_points_853 = None
        self.A_Region_segmentation_841 = None
        self.A_Number_of_single_values_349 = None
        self.A_Single_precision_type_908 = None
        self.A_Double_precision_920 = None
        self.A_Variable_909 = None
        self.A_Fence_analysis_893 = None
        self.A_Online_template_844 = None
        self.A_Online_template_873 = None
        self.A_Vertical_857 = None
        self.A_String_916 = None
        self.A_Real_time_frame_rate_894 = None
        self.A_Boolean_type_906 = None
        self.A_Image_data_set_912 = None
        self.A_Image_sample_management_876 = None
        self.A_Quick_print_870 = None
        self.A_Print_856 = None
        self.A_Open_the_situation_map_922 = None
        self.A_Fold_line_861 = None
        self.A_The_thinning_node_852 = None
        self.A_Topology_data_set_917 = None
        self.A_Capture_the_catchment_849 = None
        self.A_Extract_tile_mesh_face_838 = None
        self.A_Plug_in_upload_836 = None
        self.A_Plug_in_upload_851 = None
        self.A_Erase_out_of_boundary_tile_850 = None
        self.A_Data_research_871 = None
        self.A_Data_acquisition_847 = None
        self.A_Integer_914 = None
        self.A_Date_911 = None
        self.A_Template_customization_846 = None
        self.A_Template_customization_879 = None
        self.A_Template_database_building_839 = None
        self.A_Template_management_843 = None
        self.A_Template_management_860 = None
        self.A_Template_upload_842 = None
        self.A_Template_upload_866 = None
        self.A_Level_872 = None
        self.A_Horizontal_distance_834 = None
        self.A_Draw_and_repair_lines_867 = None
        self.A_Draw_lines_and_trim_885 = None
        self.A_Drawing_lines_and_constructing_planes_875 = None
        self.A_Picture_plane_883 = None
        self.A_Boundary_check_888 = None
        self.A_Target_statistics_904 = None
        self.A_Straight_line_869 = None
        self.A_Vector_data_set_913 = None
        self.A_Short_integer_907 = None
        self.A_Manage_bookmarks_831 = None
        self.A_Line_Style_Settings_864 = None
        self.A_Automatic_compression_903 = None
        self.A_Automatic_frame_skipping_897 = None
        self.A_Ziyou_884 = None
        self.A_Identification_837 = None
        self.A_Identification_862 = None
        self.A_Distance_832 = None
        self.A_License_plate_coding_891 = None
        self.A_Trajectory_extraction_900 = None
        self.A_Connecting_line_874 = None
        self.A_Select_line_object_to_repair_line_889 = None
        self.A_Select_line_object_trimming_865 = None
        self.A_Mosaic_dataset_910 = None
        self.A_Long_integer_921 = None
        self.A_Surface_polymerization_840 = None
        self.A_Surface_polymerization_881 = None
        self.A_Color_918 = None
        self.A_Color_table_919 = None


from huza.icons.images.icon1 import image_dict as icon1_dict


class Icon1IconHandler(IconHandler):
    def __init__(self):
        super(Icon1IconHandler, self).__init__()
        self._icon_database = icon1_dict


from huza.icons.images.icon10 import image_dict as icon10_dict


class Icon10IconHandler(IconHandler):
    def __init__(self):
        super(Icon10IconHandler, self).__init__()
        self._icon_database = icon10_dict


from huza.icons.images.icon11 import image_dict as icon11_dict


class Icon11IconHandler(IconHandler):
    def __init__(self):
        super(Icon11IconHandler, self).__init__()
        self._icon_database = icon11_dict


from huza.icons.images.icon12 import image_dict as icon12_dict


class Icon12IconHandler(IconHandler):
    def __init__(self):
        super(Icon12IconHandler, self).__init__()
        self._icon_database = icon12_dict


from huza.icons.images.icon13 import image_dict as icon13_dict


class Icon13IconHandler(IconHandler):
    def __init__(self):
        super(Icon13IconHandler, self).__init__()
        self._icon_database = icon13_dict


from huza.icons.images.icon2 import image_dict as icon2_dict


class Icon2IconHandler(IconHandler):
    def __init__(self):
        super(Icon2IconHandler, self).__init__()
        self._icon_database = icon2_dict


from huza.icons.images.icon3 import image_dict as icon3_dict


class Icon3IconHandler(IconHandler):
    def __init__(self):
        super(Icon3IconHandler, self).__init__()
        self._icon_database = icon3_dict


from huza.icons.images.icon4 import image_dict as icon4_dict


class Icon4IconHandler(IconHandler):
    def __init__(self):
        super(Icon4IconHandler, self).__init__()
        self._icon_database = icon4_dict


from huza.icons.images.icon5 import image_dict as icon5_dict


class Icon5IconHandler(IconHandler):
    def __init__(self):
        super(Icon5IconHandler, self).__init__()
        self._icon_database = icon5_dict


from huza.icons.images.icon6 import image_dict as icon6_dict


class Icon6IconHandler(IconHandler):
    def __init__(self):
        super(Icon6IconHandler, self).__init__()
        self._icon_database = icon6_dict


from huza.icons.images.icon7 import image_dict as icon7_dict


class Icon7IconHandler(IconHandler):
    def __init__(self):
        super(Icon7IconHandler, self).__init__()
        self._icon_database = icon7_dict


from huza.icons.images.icon8 import image_dict as icon8_dict


class Icon8IconHandler(IconHandler):
    def __init__(self):
        super(Icon8IconHandler, self).__init__()
        self._icon_database = icon8_dict


from huza.icons.images.icon9 import image_dict as icon9_dict


class Icon9IconHandler(IconHandler):
    def __init__(self):
        super(Icon9IconHandler, self).__init__()
        self._icon_database = icon9_dict


from huza.icons.images.cae import image_dict as cae_dict


class CaeIconHandler(IconHandler):
    def __init__(self):
        super(CaeIconHandler, self).__init__()
        self._icon_database = cae_dict


from huza.icons.images.freecad import image_dict as freecad_dict


class FreecadIconHandler(IconHandler):
    def __init__(self):
        super(FreecadIconHandler, self).__init__()
        self._icon_database = freecad_dict


from huza.icons.images.matlab import image_dict as matlab_dict


class MatlabIconHandler(IconHandler):
    def __init__(self):
        super(MatlabIconHandler, self).__init__()
        self._icon_database = matlab_dict


from huza.icons.images.paraview import image_dict as paraview_dict


class ParaviewIconHandler(IconHandler):
    def __init__(self):
        super(ParaviewIconHandler, self).__init__()
        self._icon_database = paraview_dict


from huza.icons.images.pointwise import image_dict as pointwise_dict


class PointwiseIconHandler(IconHandler):
    def __init__(self):
        super(PointwiseIconHandler, self).__init__()
        self._icon_database = pointwise_dict
