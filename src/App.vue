<template>
    <div>
        <vue-headful title="通信工线务中级考试题库 - 伟大的圣弗朗西斯科英杰" description="Ask for yingshaoxo" />
        <h5 v-if="angry==false"  style="text-align:center; margin-top:9vh; opacity: 0.4;" @click="showAnswer()">{{getCorrectRatio()}}%</h5>
        <h5 v-if="angry==true"  style="color: red; text-align:center; margin-top:9vh; opacity: 0.4;" @click="showAnswer()">{{getCorrectRatio()}}%</h5>
        <div class="box">
            <div class="question">
                <div>
                    <h5>{{qIndex + 1}}. {{data[qIndex].title}}</h5>
                    <ul>
                        <li v-for="(a, index1) in data[qIndex].items" @click="checkEvent(index1)" :class="{active: activeIndex === index1, color1: index1 === rightIndex, color2: index1 === errorIndex}">
                            <span v-if="index1 === 0" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">A</span>
                            <span v-if="index1 === 1" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">B</span>
                            <span v-if="index1 === 2" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">C</span>
                            <span v-if="index1 === 3" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">D</span>
                            <span v-if="index1 === 4" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">E</span>
                            <span v-if="index1 === 5" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">F</span>
                            <span v-if="index1 === 6" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">G</span>
                            <span v-if="index1 === 7" :class="[{sign1: index1 === rightIndex}, {sign2: index1 === errorIndex}, 'sign']">H</span> {{a}}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="btn-box">
            <div class="left">
                <div :class="[{button: qIndex !== 0}, {button1: qIndex === 0}]" @click="preEvent">上一题</div>
            </div>
            <div class="right">
                <div :class="[{button: qIndex !== data.length - 1}, {button1: qIndex === data.length - 1}]" @click="nextEvent">下一题</div>
            </div>
        </div>
        <transition name="explain">
            <div class="explain" v-show="ansState">
                <p>
                    <span style="color: #00a400;">最佳解释：</span> {{data[qIndex].reason}}
                </p>
            </div>
        </transition>
        <div style="width: 100%; height: 50px;"></div>
        <transition name="toast">
            <div class="toast" v-if="toast">
                <div class="main">{{toastText}}</div>
            </div>
        </transition>
        <div class="fixed_right" @click="listEvent"></div>
        <div class="fixed_left" @click="doWrongList"></div>
        <div class="footer">
            <!--div :class="['btn', {btn1: collectionState}]" @click="collectionEvent">{{collectionText}}</div-->
            <!--div class="btn" @click="answerEvent">看答案</div-->
            <!--div class="btn" @click="collectListEvent">收藏夹<span v-if="collectNum">({{collectNum}})</span></div-->
            <!--div class="btn" @click="errorListEvent">错题本<span v-if="errorHtmlData.length">({{errorHtmlData.length}})</span></div-->
    
            <p style="text-align:center; margin-bottom:5px; opacity: 0.2;" v-show="showNewVersion" v-b-modal.modal-1>
            </p>
            <p style="text-align:center; margin-bottom:5px; opacity: 0.2;">
                本程序由 南京铁道职业技术学院 铁道通信1702 胡英杰 制作
                </br>
                <small>徐新宇、苏宇 协助数据优化</small>
                </br>
                <small style="color:green;" v-show="showNewVersion" v-b-modal.modal-1>new version</small>
                <small style="color:green;" v-if="showNewVersion==false" @click="just_clear_storage">old version</small>
            </p>
            <div>
                <b-modal id="modal-1" ref="my-modal" title="英杰 友情提醒" centered hide-footer>
                    <p class="my-4" style="text-align: center;">升级到新题库，原有的答题数据将被清空。</p>
                    <div style="text-align:center;">
                        <b-button @click="clear_storage" variant="primary"><small>一键解决当前版本各种异常问题</small></b-button>
                    </div>
                    <div style="width: 100%; margin-top: 2vh">
                        <b-button @click="toggleModal" variant="danger" style="float: left; width: 40%; margin: 1vw">确定</b-button>
                        <b-button @click="hideModal" variant="success" style="float: right; width: 40%; margin: 1vw"">取消</b-button>
                    </div>
                </b-modal>
            </div>
        </div>
        <li-model ref="collectList" type="pop" class="collectList">
            <div slot="modalbody">
                <h5>收藏夹</h5>
                <ul>
                    <li v-for="item in collectHtmlData">
                        <div class="item right" @click="collectInEvent(item - 1)">{{item}}</div>
                    </li>
                </ul>
            </div>
            <div slot="modelfoot"></div>
        </li-model>
    
        <li-model ref="list" type="pop" class="collectList">
            <div slot="modalbody">
                <h5>答题概览</h5>
                <ul>
                    <li v-for="item in allQuestionState">
                        <div class="item" v-if="item.state === 1" @click="allQuestionEvent(item.id)">{{item.id + 1}}</div>
                        <div class="item right" v-if="item.state === 2" @click="allQuestionEvent(item.id)">{{item.id + 1}}</div>
                        <div class="item error" v-if="item.state === 3" @click="allQuestionEvent(item.id)">{{item.id + 1}}</div>
                    </li>
                </ul>
                <p style="text-align:center">
                    Made by
                    <span style="color:green;">beautifulBoys</span> and
                    <span>
                  <a style="color:green;" href="https://yingshaoxo.xyz" target="_blank">yingshaoxo</a>
                </span>
                </p>
            </div>
            <div slot="modelfoot"></div>
        </li-model>
    
        <li-model ref="error" type="pop" class="collectList">
            <div slot="modalbody">
                <h5>错题本</h5>
                <ul>
                    <li v-for="item in errorHtmlData">
                        <div class="item error" @click="errInEvent(item - 1)">{{item}}</div>
                    </li>
                </ul>
            </div>
            <div slot="modelfoot"></div>
        </li-model>
    </div>
</template>

<script>
    import data from "../data.json";
    import datav3 from "../datav3.json";
    import model from "./components/model.vue";
    export default {
        name: "app",
        components: {
            "li-model": model
        },
        data() {
            var show = true;
            var dataList = data.list;
    
            var currentUrl = window.location.pathname;
    
            var version = localStorage.getItem("version");
            if (version === "v3") {
                if (currentUrl.indexOf("/v3") >= 0) {
                    show = false;
                    dataList = datav3.list;
                } else {
                    window.open("v3/index.html", "_self");
                }
            } else if (version === null) {
                if (currentUrl.indexOf("/v3") >= 0) {
                    window.open("../index.html", "_self");
                } else {}
            }
    
            return {
                data: dataList,
                qIndex: 0,
                activeIndex: -1,
                rightIndex: -1,
                errorIndex: -1,
                questionList: [],
                ansState: false,
                showNewVersion: show,
                collectionList: [],
                collectHtmlData: [],
                collectNum: 0,
                errorHtmlData: [],
                errNum: 0,
                collectionState: false,
                collectionText: "收藏",
                toast: false,
                toastText: "",
                allQuestionState: [],
                angry: false,
                angry_wrong_list: []
            };
        },
        watch: {
            qIndex(n, o) {
                if (this.angry == false) {
                    this.qIndex = n;
                    this.qIndexChange();
        
                    console.log("qIndex changed!");
                    localStorage.setItem("qIndex", JSON.stringify(this.qIndex));
                }
            },
    
            activeIndex: {
                handler() {
                    if (this.angry == false) {
                        console.log("activeIndex changed!");
                        localStorage.setItem("activeIndex", JSON.stringify(this.activeIndex));
                    }
                },
                deep: true
            },
    
            rightIndex: {
                handler() {
                    if (this.angry == false) {
                        console.log("rightIndex changed!");
                        localStorage.setItem("rightIndex", JSON.stringify(this.rightIndex));
                    }
                },
                deep: true
            },
    
            errorIndex: {
                handler() {
                    if (this.angry == false) {
                        console.log("errorIndex changed!");
                        localStorage.setItem("errorIndex", JSON.stringify(this.errorIndex));
                    }
                },
                deep: true
            },
    
            questionList: {
                handler() {
                    if (this.angry == false) {
                        console.log("questionList changed!");
                        localStorage.setItem("questionList", JSON.stringify(this.questionList));
                    }
                },
                deep: true
            },
    
            allQuestionState: {
                handler() {
                    console.log("allQuestionState changed!");
                    localStorage.setItem(
                        "allQuestionState",
                        JSON.stringify(this.allQuestionState)
                    );
                },
                deep: true
            }
        },
        mounted() {
            for (var i = 0; i < this.data.length; i++) {
                this.collectionList.push(false);
                this.allQuestionState.push({
                    id: i,
                    state: 1
                }); // state 1:未做   2:对    3:错
            }

            console.log("App mounted!");

            if (localStorage.getItem("qIndex")) {
                this.qIndex = JSON.parse(localStorage.getItem("qIndex"));
            }

            if (localStorage.getItem("activeIndex")) {
                this.activeIndex = JSON.parse(localStorage.getItem("activeIndex"));
            }

            if (localStorage.getItem("rightIndex")) {
                this.rightIndex = JSON.parse(localStorage.getItem("rightIndex"));
            }

            if (localStorage.getItem("errorIndex")) {
                this.errorIndex = JSON.parse(localStorage.getItem("errorIndex"));
            }

            if (localStorage.getItem("questionList")) {
                this.questionList = JSON.parse(localStorage.getItem("questionList"));
            }

            if (localStorage.getItem("allQuestionState")) {
                this.allQuestionState = JSON.parse(
                    localStorage.getItem("allQuestionState")
                );
            }
        },
        methods: {
            showModal() {
                this.$refs["my-modal"].show();
            },
            hideModal() {
                this.$refs["my-modal"].hide();
            },
            toggleModal() {
                this.$refs["my-modal"].toggle("#toggle-btn");
                localStorage.clear();
                localStorage.setItem("version", "v3");
    
                setTimeout(function() {
                    window.open("v3/index.html", "_self");
                }, 1000);
            },

            clear_storage() {
                this.$refs["my-modal"].toggle("#toggle-btn");
                localStorage.clear();
                setTimeout(function() {
                    location.reload();
                }, 1000);
            },

            just_clear_storage() {
                localStorage.clear();
                setTimeout(function() {
                    location.reload();
                }, 1000);
            },

            getCorrectRatio() {
                if (this.allQuestionState != []) {
                    var all_you_have_answered = 0;
                    var correct_num = 0;
                    this.allQuestionState.forEach((obj) => {
                        if (obj.state != 1) {
                            all_you_have_answered += 1;
                            if (obj.state == 2) {
                                correct_num += 1;
                            }
                        }
                    })
                    if (all_you_have_answered != 0) {
                        return Math.trunc((correct_num/all_you_have_answered)*100)
                    } else {
                        return 0
                    }
                }
            },

            showAnswer() {
                this.nextEvent();

                var num = this.data[this.qIndex].answer;
                this.rightIndex = num;
                this.questionList[this.qIndex] = {
                    userAns: num,
                    rightAns: num
                };

                //this.allQuestionState[this.qIndex].state = 2;
            },

            doWrongList() {
                var could_do_it = false;
                this.questionList = [];
                for (var i = 0; i < this.data.length; i++) {
                    if (this.allQuestionState[i].state == 3) {
                        if (this.angry_wrong_list.indexOf(i) > -1) {
                            continue;
                        } else {
                            could_do_it = true;
                            this.qIndex = i;
                            this.activeIndex = -1;
                            this.rightIndex = -1;
                            this.errorIndex = -1;
                            this.ansState = false;
                            break;
                        }
                    }
                };
                if (could_do_it == true) {
                    this.angry = true;
                } else {
                    if (this.angry == true) {
                        //location.reload();
                        if (localStorage.getItem("qIndex")) {
                            var saved_qindex = JSON.parse(localStorage.getItem("qIndex"));
                            if (saved_qindex == this.qIndex) {
                                this.qIndex = saved_qindex + 1;
                            } else {
                                this.qIndex = JSON.parse(localStorage.getItem("qIndex"));
                            }
                        }
                        this.activeIndex = -1;
                        this.rightIndex = -1;
                        this.errorIndex = -1;
                        this.ansState = false;

                        this.angry_wrong_list = [];
                    }
                    this.angry = false;
                }
            },
    
            checkEvent(num) {
                if (!this.questionList[this.qIndex]) {
                    // 判断当前题目是否做过
                    // check if you have answered this before
                    this.activeIndex = num;
                    if (this.data[this.qIndex].answer === num) {
                        // 做对了
                        this.rightIndex = num;
                        this.questionList[this.qIndex] = {
                            userAns: num,
                            rightAns: num
                        };
                        this.allQuestionState[this.qIndex].state = 2;
                        if (this.angry == false) {
                            setTimeout(() => {
                                this.nextEvent();
                            }, 500);
                        } else {
                            setTimeout(() => {
                                this.nextEvent();
                            }, 1000);
                        }
                    } else {
                        // 做错了
                        if (this.angry == true) {
                            this.angry_wrong_list.push(this.qIndex);
                        }
                        this.errorIndex = num;
                        this.rightIndex = this.data[this.qIndex].answer;
                        this.questionList[this.qIndex] = {
                            userAns: num,
                            rightAns: this.data[this.qIndex].answer
                        };
                        this.errorHtmlData.push(this.qIndex + 1);
                        this.allQuestionState[this.qIndex].state = 3;
                    }
                }
            },
            preEvent() {
                if (this.qIndex !== 0) {
                    this.qIndex -= 1;
                    this.activeIndex = -1;
                    this.rightIndex = -1;
                    this.errorIndex = -1;
                    this.ansState = false;
                }
            },
            qIndexChange() {
                this.activeIndex = -1;
                this.rightIndex = -1;
                this.errorIndex = -1;
                if (this.questionList[this.qIndex]) {
                    // 已答列表是否存在
                    if (
                        this.questionList[this.qIndex].rightAns ===
                        this.questionList[this.qIndex].userAns
                    ) {
                        // 答案是否正确
                        this.rightIndex = this.questionList[this.qIndex].rightAns;
                    } else {
                        this.rightIndex = this.questionList[this.qIndex].rightAns;
                        this.errorIndex = this.questionList[this.qIndex].userAns;
                    }
                }
                if (this.collectionList[this.qIndex]) {
                    // 判断是否收藏
                    this.collectionState = true;
                    this.collectionText = "取消收藏";
                } else {
                    this.collectionState = false;
                    this.collectionText = "收藏";
                }
            },
            nextEvent() {
                if (this.angry == false) {
                    if (this.data.length > this.qIndex + 1) {
                        this.qIndex += 1;
                        this.activeIndex = -1;
                        this.rightIndex = -1;
                        this.errorIndex = -1;
                        this.ansState = false;
                    }
                } else {
                    this.doWrongList();
                }
            },
            answerEvent() {
                if (this.questionList[this.qIndex]) this.ansState = !this.ansState;
                else this.showToast("未做题目不能看答案");
            },
            collectionEvent() {
                if (this.collectionState) {
                    this.collectionList[this.qIndex] = false;
                    this.collectionState = !this.collectionState;
                    this.collectionText = "收藏";
                } else {
                    this.collectionList[this.qIndex] = true;
                    this.collectionState = !this.collectionState;
                    this.collectionText = "取消收藏";
                }
                this.collectNum = this.getCollectList().length;
            },
            getCollectList() {
                var a = [];
                for (var i = 0; i < this.collectionList.length; i++) {
                    if (this.collectionList[i]) {
                        a.push(i + 1);
                    }
                }
                return a;
            },
            collectListEvent() {
                this.collectHtmlData = this.getCollectList();
                if (this.collectHtmlData.length > 0) {
                    this.$refs.collectList.modelOpen();
                } else {
                    this.showToast("您当前还没有收藏题目");
                }
            },
            showToast(str) {
                var me = this;
                me.toast = true;
                me.toastText = str;
                setTimeout(function() {
                    me.toast = false;
                }, 2000);
            },
            listEvent() {
                this.$refs.list.modelOpen();
            },
            errorListEvent() {
                if (this.errorHtmlData.length > 0) this.$refs.error.modelOpen();
                else this.showToast("您当前还没有错题");
            },
            errInEvent(num) {
                this.$refs.error.modelClose();
                this.qIndex = num;
            },
            collectInEvent(num) {
                this.$refs.collectList.modelClose();
                this.qIndex = num;
            },
            allQuestionEvent(num) {
                this.$refs.list.modelClose();
                this.qIndex = num;
            }
        }
    };
</script>

<style lang="less" scoped>
    .fixed_right {
        width: 50px;
        height: 50px;
        background: #fff url(./images/list.svg) no-repeat center center;
        background-size: 30px;
        position: fixed;
        top: 80%;
        right: 15px;
        border-radius: 50%;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        &:active {
            background: #eee url(./images/list.svg) no-repeat center center;
            background-size: 30px;
        }
    }

    .fixed_left {
        width: 50px;
        height: 50px;
        background: #fff url(./images/angry.svg) no-repeat center center;
        background-size: 30px;
        position: fixed;
        top: 80%;
        left: 15px;
        border-radius: 50%;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        &:active {
            background: #eee url(./images/angry.svg) no-repeat center center;
            background-size: 30px;
        }
    }
    
    .collectList {
        h5 {
            margin: 0;
            padding-top: 15px;
            line-height: 25px;
            text-align: center;
            color: #444;
        }
        ul {
            padding: 15px 0;
            margin: 0 auto;
            width: 94%;
            font-size: 0;
            height: 60vh;
            overflow: hidden;
            overflow-y: scroll;
            li {
                width: 20%;
                height: 60px;
                display: inline-block;
                position: relative;
                .item {
                    width: 40px;
                    height: 40px;
                    border: 1px solid #aaa;
                    border-radius: 50%;
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    margin: auto;
                    font-size: 18px;
                    color: #333;
                    line-height: 40px;
                    text-align: center;
                    &:active {
                        background: #ccc;
                        color: #333;
                    }
                    &.right {
                        color: #00a400;
                        border: 1px solid #00a400;
                        background: rgba(0, 164, 0, 0.17);
                        &:active {
                            background: #00a400;
                            color: #fff;
                        }
                    }
                    &.error {
                        color: #e8571b;
                        border: 1px solid #e8571b;
                        background: rgba(255, 96, 30, 0.17);
                        &:active {
                            background: #e8571b;
                            color: #fff;
                        }
                    }
                }
            }
        }
    }
    
    .toast {
        width: 100%;
        position: fixed;
        top: 70%;
        min-height: 30px;
        opacity: 1;
        font-family: "Microsoft YaHei";
        color: #fff;
        font-size: 14px;
        &.toast-enter-active,
        &.toast-leave-active {
            transition: opacity 0.5s;
        }
        &.toast-enter,
        &.toast-leave-to {
            opacity: 0;
        }
        .main {
            background: rgba(0, 0, 0, 0.6);
            max-width: 70%;
            height: 100%;
            border-radius: 5px;
            margin: 0 auto;
            text-align: center;
            line-height: 20px;
            padding: 5px 10px;
        }
    }
    
    .footer {
        width: 100%;
        position: fixed;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: "Microsoft YaHei";
        background: #fff;
        font-size: 15px;
        .btn {
            width: 100%;
            text-align: center;
            border-right: 1px solid #ddd;
            border-top: 1px solid #ddd;
            &:nth-last-child(1) {
                border-right: none;
            }
            &:active {
                background: #ddd;
            }
            &.btn1 {
                color: #00a400;
            }
        }
    }
    
    .explain {
        background: #fff;
        width: 100%;
        font-family: "Microsoft YaHei";
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        font-size: 15px;
        opacity: 1;
        &.explain-enter-active,
        &.explain-leave-active {
            transition: opacity 0.5s;
        }
        &.explain-enter,
        &.explain-leave-to {
            opacity: 0;
        }
        p {
            padding: 10px;
            box-sizing: border-box;
            line-height: 25px;
        }
    }
    
    .btn-box {
        width: 100%;
        height: 40px;
        display: flex;
        margin: 10vh 0;
        font-size: 15px;
        font-family: "Microsoft YaHei";
        .left {
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .right {
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .button {
            width: 80%;
            line-height: 40px;
            background: #00a400;
            display: block;
            text-align: center;
            color: #fff;
            border-radius: 5px;
            &:active {
                background: green;
            }
        }
        .button1 {
            width: 80%;
            line-height: 40px;
            display: block;
            text-align: center;
            border-radius: 5px;
            background: #ddd;
            color: #333;
        }
    }
    
    .box {
        width: 100%;
        position: relative;
        margin-top: 9vh;
        margin-bottom: 10vh;
        align-items: center;
        font-family: "Microsoft YaHei";
        font-size: 2vh;
        .question {
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 10px;
            box-sizing: border-box;
            h5 {
                font-weight: 500;
                line-height: 25px;
                padding: 10px;
                box-sizing: border-box;
                margin: 0;
                font-size: 2vh;
            }
            ul {
                padding: 0;
                margin: 0;
                li {
                    list-style-type: none;
                    line-height: 40px;
                    text-indent: 10px;
                    &.active {
                        background: rgba(73, 158, 255, 0.12);
                    }
                    &.color1 {
                        color: #00a400;
                    }
                    &.color2 {
                        color: #e8571b;
                    }
                    .sign {
                        width: 18px;
                        height: 18px;
                        line-height: 16px;
                        border-radius: 50%;
                        display: inline-block;
                        text-indent: 4.5px;
                        border: 1px solid #555;
                        color: #333;
                        font-size: 12px;
                        &.sign1 {
                            /*成功*/
                            color: #fff;
                            background: #00a400;
                            border: 1px solid #00a400;
                        }
                        &.sign2 {
                            /*失败*/
                            color: #fff;
                            background: #e8571b;
                            border: 1px solid #e8571b;
                        }
                    }
                }
            }
        }
    }
</style>
