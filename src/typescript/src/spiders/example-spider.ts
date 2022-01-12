import Spider from "../core/spiders/spider";
import RmqPipeline from "../pipelines/rmq-pipeline";
import { HTTPResponse } from "puppeteer";
import gotoWithRetries from "../utils/puppeteer/goto-with-retries";
import ProcessArguments from "../interfaces/argv";

import ExampleSpiderProperties from "../interfaces/example-spider-properties";
import ErrorItem from "../items/output-item/error-item";
import ExampleInputItem from "../items/input-item/example-input-item";
import ExampleOutputItem from "../items/output-item/example-output-item";
import {mobileproxyChangeIp, mobileproxyChangeEquipment} from "../utils/mobileproxy-manager";


export default class ExampleSpider extends Spider {
    public static spiderName: string = 'example';
    public taskQueueName = this.settings.EXAMPLE_SPIDER_TASK_QUEUE;

    getCustomSettingsProperties(): ExampleSpiderProperties {
        return {
            pipelines: [
                RmqPipeline,
            ],
        };
    }

    convertArgsToInputMessage(args: ProcessArguments | ExampleInputItem): ExampleInputItem {
        return new ExampleInputItem(args.url);
    }

    async* process(inputMessage: ExampleInputItem): AsyncIterableIterator<ExampleOutputItem | ErrorItem> {
        let error: Error | unknown;
        let response: HTTPResponse | null = null;
        let url = inputMessage.url;

        for (let attempt = 0; attempt < 5; attempt++) {
            try {
                response = await gotoWithRetries(this.page!, url, { waitUntil: ["networkidle0", "load", "domcontentloaded"] });
                if (!!response) {
                    this.logger.debug(`Crawled ${response.url()} (${response.status()})`);
                } else {
                    this.logger.debug(`Crawled ${url} (null)`);
                }

                if (await this.isErrorResponseStatusCode(response)) {
                    const status = response ? response.status() : 'unknown';
                    throw new Error(`received response with status code "${status}"`);
                }

                // extractData
                this.logger.info(`Parsed ${url}`);
                this.logger.info(await response?.text());
                //this.logger.info(await mobileproxyChangeIp('b28af936fd9de0cd75635406befc53b9'));
                //this.logger.info(await mobileproxyChangeEquipment('664742bbcf33dbd02971608d47a525fc', '55117'))
            } catch (e) {
                this.logger.warn(e);
                error = e;
                await this.restartBrowser();
            }
        }
        return;
    }

    async isErrorResponseStatusCode(response: HTTPResponse | null): Promise<boolean> {
        if (!!response) {
            const status = response.status();
            return status >= 400;
        }
        return false;
    }
}
