import axios from "axios";

const MOBILEPROXY_RELOAD_IP_ENDPOINT: string = "https://mobileproxy.space/reload.html"
const MOBILEPROXY_CHANGE_EQUIPMENT_ENDPOINT: string = "https://mobileproxy.space/api.html?command=change_equipment"
const USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

export async function mobileproxyChangeIp(proxyKey: string): Promise<boolean>{
    const mobileproxy_response = await axios.get(MOBILEPROXY_RELOAD_IP_ENDPOINT, {
        params: {
            "proxy_key": proxyKey,
            "format": "json"
        },
        headers: {
            "User-Agent": USER_AGENT
        }
    });
    return mobileproxy_response.data
}

export async function mobileproxyChangeEquipment(apiToken:string, proxyId: string, geoId: string = '', operator: string = ''): Promise<boolean>{

    const mobileproxy_response = await axios.get(MOBILEPROXY_CHANGE_EQUIPMENT_ENDPOINT, {
        params: {
            "operator": operator,
            "geoid": geoId,
            "proxy_id": proxyId,
            "format": "json"
        },
        headers: {
            "Authorization": "Bearer "+ apiToken,
            "User-Agent": USER_AGENT
        }
    });

    return mobileproxy_response.data
}
