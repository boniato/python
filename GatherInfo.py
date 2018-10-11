def collect_lent(ym, lawd_cd):

    API_KEY = (제공받은 API키)

    url="http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent"


    # &numOfRows=1000"+

    url=url+"?&LAWD_CD="+lawd_cd+"&DEAL_YMD="+ym+"&serviceKey="+API_KEY


    # webbrowser.open(url)

    resultXML = urlopen(url)

    result = resultXML.read()

    xmlsoup = BeautifulSoup(result, 'lxml-xml')


    te=xmlsoup.findAll("item")

    sil=pd.DataFrame()


    for t in te:

        build_y=t.find("건축년도").text

        year=t.find("년").text

        month=t.find("월").text

        day=t.find("일").text

        dong=t.find("법정동").text

        bo_price=t.find("보증금액").text

        mo_price=t.find("월세금액").text

        apt_nm=t.find("아파트").text

        size=t.find("전용면적").text

        try:

            jibun=t.find("지번").text

        except:

            jibun=""


        ji_code=t.find("지역코드").text

        floor=t.find("층").text


        temp = pd.DataFrame(([[build_y,year,month,day,dong,bo_price,mo_price,apt_nm,size,jibun,ji_code,floor]]), columns=["build_y","year","month","day","dong","bo_price","mo_price","apt_nm","size","jibun","ji_code","floor"])

        sil=pd.concat([sil,temp])


    sil=sil.reset_index(drop=True)

    return sil
