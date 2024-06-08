<template>
    <div>
        <h1> {{ title }}</h1>
        
        <p>最后一次接收数据的时间：{{ lastReceivedTime }}</p>
        <p>更新倒计时：{{ countdown }}</p>
        <button @click="toggleAutoUpdate">
            {{ autoUpdate ? '关闭自动更新' : '开启自动更新' }}
        </button>

        <table>
            <thead>
                <tr>
                    <th></th>
                    <th v-for="date in settleDates" :key="date">{{ formatDate(date) }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="price in strikePrices" :key="price">
                    <td>{{ price }}</td>
                    <td v-for="date in settleDates" :key="date" :class="getAprClass(getAprValue(price, date))">
                        {{ getAprString(getAprValue(price, date)) }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {

    props: {
        
        title: String,
        url: String,
        price_sort_desc: Boolean,
    },
    data() {
        return {
            data: {
                total: 0,
                list: []
            },
            strikePrices: [],
            settleDates: [],
            lastReceivedTime: '',
            countdown:10,
            ws:null,
            autoUpdate: true,
            intervalId: null,
        };
    },
    mounted() {
        this.ws = new WebSocket(this.url);
        this.connectWebSocket();
        this.startCountdown();
    },
    methods: {
        connectWebSocket() {
            // const ws = new WebSocket('ws://localhost:8000/ws2'); // 替换为你的WebSocket服务器地址
            const ws = this.ws;
            ws.onmessage = (event) => {
                const serverData = JSON.parse(event.data);
                this.updateDataList(serverData.list);
                this.updateTableData();
                this.lastReceivedTime = new Date().toLocaleString(); // 更新接收数据的时间

            };
            ws.onerror = (error) => {
                console.error('WebSocket Error: ', error);
            };
            ws.onclose = () => {
                console.log('WebSocket connection closed');
            };
        },
        updateDataList(newList) {
            const updatedList = [...this.data.list];

            newList.forEach(newItem => {
                const index = updatedList.findIndex(item => item.id === newItem.id);
                if (index !== -1) {
                    // 更新已有的项
                    updatedList[index] = newItem;
                } else {
                    // 添加新的项
                    updatedList.push(newItem);
                }
            });

            this.data.list = updatedList;
        },
        updateTableData() {
            const strikePricesSet = new Set();
            const settleDatesSet = new Set();

            this.data.list.forEach(item => {
                strikePricesSet.add(item.strikePrice);
                settleDatesSet.add(item.settleDate);
            });

            this.strikePrices = Array.from(strikePricesSet).sort((a, b) => parseFloat(a) - parseFloat(b));
            if (this.price_sort_desc) {
                this.strikePrices = this.strikePrices.reverse();
            }
            this.settleDates = Array.from(settleDatesSet).sort((a, b) => a - b);
        },
        getAprValue(strikePrice, settleDate) {
            const item = this.data.list.find(
                item => item.strikePrice === strikePrice && item.settleDate === settleDate
            );
            // return item ? this.toPercentageString(item.apr) : '-';
            return item ? item.apr : null;
        },
        getAprString(apr){
            return apr ? this.toPercentageString(apr) : '-';
        },
        toPercentageString(number) {
            const percentage = (number * 100).toFixed(2);
            return `${percentage}%`;
        },
        formatDate(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleDateString();
        },
        startCountdown() {
            this.stopCountdown(); // 确保之前的计时器被清除
            this.countdown = 10;
            this.intervalId = setInterval(() => {
                if (this.autoUpdate) {
                    this.countdown--;
                    if (this.countdown === 0) {
                        this.sendCurrentTime();
                        this.countdown = 10;
                    }
                }
            }, 1000);
        },
        stopCountdown() {
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        },
        sendCurrentTime() {
            const currentTime = new Date().toISOString();
            this.ws.send(currentTime);
        },
    
        toggleAutoUpdate() {
            // console.log("toggleAutoUpdate");
            // alert("toggleAutoUpdate");

            this.autoUpdate = !this.autoUpdate;
            if (this.autoUpdate) {
                this.startCountdown();
            } else {
                this.stopCountdown();
            }
        },
        getAprClass(apr) {
            
            if (apr == null){
                return "";
            }
            apr = apr * 100;
            if (apr >= 0 && apr < 5) {
                return 'apr-0-5';
            } else if (apr >= 5 && apr < 10) {
                return 'apr-5-10';
            } else if (apr >= 10 && apr < 15) {
                return 'apr-10-15';
            } else if (apr >= 15 && apr < 20) {
                return 'apr-15-20';
            } else if (apr >= 20 && apr < 25) {
                return 'apr-20-25';
            } else if (apr >= 25 && apr < 30) {
                return 'apr-25-30';
            } else if (apr >= 30 && apr < 35) {
                return 'apr-30-35';
            } else if (apr >= 35 && apr < 40) {
                return 'apr-35-40';
            } else if (apr >= 40 && apr < 45) {
                return 'apr-40-45';
            } else if (apr >= 45 && apr < 50) {
                return 'apr-45-50';
            } else {
                return 'apr-50-plus';
            }
        },
        beforeDestroy() {
            if (this.ws) {
                this.ws.close();
            }
        }
    }
};
</script>

<style scoped>
h1 {
    font-size: 24px;
    margin-bottom: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
}

th {
    background-color: #f2f2f2;
    text-align: left;
}

.apr-0-5 {
    background-color: rgba(144, 238, 144, 0.1);
    /* 浅绿色 */
}

.apr-5-10 {
    background-color: rgba(111, 218, 193, 0.2);
    /* 绿色稍深 */
}

.apr-10-15 {
    background-color: rgba(111, 218, 193, 0.4);
    /* 绿色更深 */
}

.apr-15-20 {
    background-color: rgba(111, 218, 154, 0.5);
    /* 绿色更深 */
}

.apr-20-25 {
    background-color: rgba(221, 232, 117, 0.5);
    /* 深绿色 */
}

.apr-25-30 {
    background-color: rgba(204, 230, 122, 0.55);
    /* 更深绿色 */
}

.apr-30-35 {
    background-color: rgba(218, 232, 109, 0.7);
    /* 更深绿色 */
}

.apr-35-40 {
    background-color: rgba(228, 217, 93, 0.8);
    /* 更深绿色 */
}

.apr-40-45 {
    background-color: rgba(229, 190, 83, 0.9);
    /* 更深绿色 */
}

.apr-45-50 {
    background-color: rgba(233, 142, 73, 1);
    
}

.apr-50-plus {
    background-color: rgb(231, 87, 62);
    /* 更深蓝色 */
}

</style>