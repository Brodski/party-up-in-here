from __future__ import unicode_literals
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from typing import List
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.webdriver import WebDriver
import os
import re
import time
from App_Configs import App_Configs
from Save_State import Save_State
import random

class Creator:
    
    cookie_COPPA = {
        'name': 'needCOPPA',
        'value': 'false',
        'domain': '.webtoons.com'
    }
    usernames = ["alphafox","amazingjazz","angrybird","applerider","aquawolf","aspiringcoder","autumndream","backpacker","badgerlover","beachcomber","beardboss","beautifulmind","bestbud","bigdreamer","birdwatcher","blackbelt","blackcat","bluesky","butterfly","californiagal","camerashy","candycane","captainamerica","carrottop","catlover","chasingdreams","cheesehead","cherryblossom","chessmaster","chicagolife","chocolateaddict","citysoul","climbinghigh","coffeeholic","collegekid","comicbooknerd","coolbreeze","cosmicdreamer","countrylife","crazydoglady","creativeforce","crimsonking","crossfitjunkie","crystalclear","dancingqueen","darkhorse","daydreamer","deepspace","desertflower","diamondgirl","divein","doglover","dragonfly","dreamchaser","dreamweaver","drummingirl","duskrunner","earlybird","eastcoast","electricguitar","emeraldgreen","endlessadventures","eternaloptimist","explorer","fairydust","fallenangel","familyman","fancyfeast","fastlane","featheredfriend","fieryred","fifthelement","fireball","firefly","fisherman","flamingo","flashback","floralprint","flowerchild","flyinghigh","forevergreen","fossilhunter","freebird","freedomfighter","freshstart","frontrow","funkyfresh","futuremillionaire","galacticexplorer","gardenlover","geekygirl","gemstone","ghosthunter","gingerbread","givingheart","glitterbomb","gogetter","goldcoast","goldenretriever","goodvibesonly","gratefulheart","greatgatsby","greeneyedgirl","guitarhero","harvestmoon","hawaiilife","heartbreaker","heavymetal","highfives","hiphoppin","honeybadger","horselover","hotchocolate","humblebeginnings","huntingseason","icequeen","imagination","infinitypool","innerpeace","inspiration","ironman","islandlife","ivorytower","jazzhands","OtakuOracle","MangaMaster","ChibiChampion","TsundereTitan","KawaiiKnight","SailorSenshi","ShinigamiShadow","ShoujoStar","MechaMaverick","KaijuKing","NarutoNinja","OnePiecePirate","TitanTamer","AlchemistAce","GhibliGuru","SpiritedSpirit","SenpaiSupreme","DeathNoteDiva","AttackOnOtaku","FullmetalFanatic","SaiyanScholar","JutsuJedi","ZanpakutoZealot","DragonBallDynamo","CosplayCrusader","TotoroSpirit","JellalFernandes","AstaWarrior","AkihiroSword","AkiraSoul","AllukaZoldyck","AsunaKnight","ByakuyaKuchiki","CielPhantomhive","ChikaFujiwara","DazaiOsamu","DekuHero","ErenYeager","ErzaScarlet","EdwardElric","GintokiSakata","GonFreecss","GrayFullbuster","GohanSSJ2","HikariYagami","HisokaMorow","HinataHyuga","HieiJagan","InuyashaDog","ItachiUchiha","IchigoKurosaki","JotaroKujo","JuviaLockser","KakashiHatake","KilluaZoldyck","KatsukiBakugo","KenshinHimura","LelouchLamperouge","LucyHeartfilia","LightYagami","LeviAckerman","MikasaAckerman","MakaAlbarn","MidoriyaIzuku","NamiNavigator","NarutoUzumaki","NatsuDragneel","NezukoKamado","OchacoUraraka","ObitoUchiha","RenjiAbarai","RukiaKuchiki","RoronoaZoro","RyukoMatoi","SaberFate","SaitamaOnePunch","ShotoTodoroki","SpikeSpiegel","SanjiBlackleg","SakuraHaruno","SasukeUchiha","ShinichiKudo","SousukeSagara","ShikamaruNara","ShinyaKogami","ShouyouHinata","TodorokiShoto","TrafalgarLaw","VegetaPrince","YugiMuto","YuYuHakusho","YusukeUrameshi","ZeroKiryu","ZerefDragneel","AlphonseElric","AllenWalker","ArminArlert","AyameSoma","AsukaLangley","Belldandy","ByakkoSuzaku","CCCode","CeltySturluson","ChopperTonyTony","DIOBrando","EchidnaWitch","ErinaNakiri","EtoYoshimura","FayeValentine","FujiwaraNoSai","GajeelRedfox","GasaiYuno","GriffithFemto","HachimanHikigaya","HajimeIppo","HanekawaTsubasa","HaruhiSuzumiya","HatsuneMiku","HeiDark","HoloWolf","HomuraAkemi","HitsugayaToshiro","IbaraShiozaki","IzayaOri","JosukeHigashikata","JunpeiHyoudou","JibrilFlugel","KaedeKayano","KagomeHigurashi","KallenStadtfeld","KanekiKen","KanadeTachibana","KazumaSatou","KibaInuzuka","KiritoBlackSword","KiyotakaAyanokouji","KonanPaperAngel","KoroSensei","KurisuMakise","KyokoSakura","LuffyMonkeyD","LightHoshikawa","MadaraUchiha","MeguminExplosion","MeliodasDragon","MioAkiyama","MiraiKuriyama","MomoYaoyorozu","NagisaShiota","NanamiMomozono","NanaOsaki","NatsuhiUshiromiya","NiaTeppelin","NicoRobin","OgaTatsumi","OkabeRintarou","OrihimeInoue","OsamuDazai","RizaHawkeye","RockLee","RoyMustang","RuiTachibana","RyoukoAsakura","SaberAlter","SadakoYamamura","SangoDemonSlayer","SayaKisaragi","SeiyaKou","SenkuIshigami","ShinobuKochou","ShionSonozaki","SubaruNatsuki","SuzakuKururugi","TaigaAisaka","TetsuoShima","TsubasaOzora","TaichiYagami","TrafalgarDWater","TsunadeSama","TsubakiNakatsukasa","UryuuIshida","UsagiTsukino","UtaTokyoGhoul","UltearMilkovich","UzuiTengen","VegetaSaiyanPrince","VashTheStampede","VioletEvergarden","VictorNikiforov","VanessaEnoteca","WhitebeardEdward","WendyMarvell","WinryRockbell","WrathFullmetal","WatashiJinrui","XerxesBreak","X1999_","XanxusVaria","XenoviaQuarta","XingkeLi","YamiSukehiro","YatoGod","YuichiroHyakuya","YokoLittner","YunoGasai","ZerefDragneel","ZeroTwo","ZenitsuAgatsuma","ZoroRoronoa","ZidaneTribal","PixelPioneer","MysticMaverick","QuantumQuirk","NeonNavigator","AstroAdept","BinaryBard","CosmicCrafter","DigitalDrifter","EchoEnigma","FrostFable","GlitchGuru","HolographicHero","InfinityIllusion","JazzyJuggernaut","KrypticKnight","LunarLegend","MatrixMystic","NebulaNomad","OmegaOrbit","PhantomPhoenix","QuantumQuester","RetroRanger","StellarSorcerer","TerraTechie","UltraUnicorn","VortexVanguard","WarpWizard","XenonXylophonist","YonderYogi","ZenithZephyr","OtakuOverlord","SaiyanSage","PixelPilgrim","ShinobiShadow","MageOfMana","TitanTactician","HikikomoriHero","AkumaAssassin","ChocoboChampion","KitsuneKnight","MechaMystic","NekoNavigator","OniOutlaw","PaladinOfPandora","QuestingQuirk","RoninRanger","SenpaiSniper","TsundereTitan","ValkyrieVanguard","WitchOfWyverns","YandereYielder","ZanpakutoZealot","GachaGuru","EsperEmissary","DokiDuelist","LancerOfLight","MoogleMage","NoctisNemesis","OtomeOracle"]

    def __init__(self, driver: WebDriver, **kwargs):
        print("###############################################################")
        print("##############        Creator - init()        #################")
        print("###############################################################")
        self.driver             = driver
        self.email              = App_Configs.init['EMAIL']
        self.pw                 = App_Configs.init['PWORD']
        self.create_start       = App_Configs.init['CREATE_BOT_START']
        self.create_end_before  = App_Configs.init['CREATE_BOT_END_BEFORE']
        if App_Configs.create_state['email_index_finished']:
            self.create_start = App_Configs.create_state['email_index_finished'] + 1

        print("     Creator - email           ", self.email)
        print("     Creator - pw              ", self.pw)
        print("     Creator - like_start      ", self.create_start)
        print("     Creator - like_end_before ", self.create_end_before)

    def run(self):
        for i in range (self.create_start, self.create_end_before):
            print(i)
            self.create_accounts(i)
            App_Configs.create_state['email_index_finished'] = i
            Save_State.update_state_file()

    def create_accounts(self, count):
        login_url = f'https://www.webtoons.com/member/join?loginType=EMAIL'
        limit = 2
        username_rng = random.choice(self.usernames) + str(random.randint(1,999))
        email_name = self.email.split('@')[0]
        domain   = self.email.split('@')[1]

        email_w_count = f"{email_name}+xxx{count}@{domain}" # supergera+12@gmail.com
        print(email_w_count)

        self.driver.get(login_url)
        self.driver.add_cookie(self.cookie_COPPA)
        time.sleep(2)

        email_clickable         = self.driver.find_element(By.ID, "email")
        pw1Input_clickable      = self.driver.find_element(By.ID, "pw")
        pw1Input2_clickable     = self.driver.find_element(By.ID, "retype_pw")
        nicknameInput_clickable = self.driver.find_element(By.ID, "nickname")
        submit_clickable        = self.driver.find_element(By.CLASS_NAME, "NPI\=a\:signup")
        
        def rng_wait():
            return random.uniform(.1,3)

        ActionChains(self.driver) \
            .click(email_clickable).send_keys(email_w_count).pause(rng_wait()) \
            .click(pw1Input_clickable).send_keys(self.pw).pause(rng_wait()) \
            .click(pw1Input2_clickable).send_keys(self.pw).pause(rng_wait()) \
            .click(nicknameInput_clickable).send_keys(username_rng).pause(rng_wait()) \
            .click(submit_clickable).pause(rng_wait()) \
            .perform()
        
        element = self.driver.find_element(By.CLASS_NAME, "_joinSuccessLayer")
        wait_elapsed = 0
        is_display_none = True
        while is_display_none:
            is_display_none = "display: none" in element.get_attribute('style')
            wait_elapsed = wait_elapsed + 0.2
            print("creating account... ", wait_elapsed)
            time.sleep(wait_elapsed)
            if wait_elapsed >= limit:
                break
        print("END!")