<template>
  <v-app>
    <v-main>
      <v-app-bar elevation="1" rounded>
        <template v-slot:prepend>
          <v-app-bar-nav-icon></v-app-bar-nav-icon>
        </template>
        <v-app-bar-title>FileAgent</v-app-bar-title>
      </v-app-bar>
      <v-snackbar v-model="snackbar.show" rounded="pill">
        {{snackbar.text}}
        <template v-slot:actions>
          <v-btn color="white" variant="text" icon="mdi-close" @click="snackbar.show=false"></v-btn>
        </template>
      </v-snackbar>
      <v-dialog v-model="dialogList.keywords" width="auto">
        <v-card>
          <v-card-title>输入对关键词的描述</v-card-title>
          <v-card-subtitle>包括关键词范围等，也可指定关键词供模型选择。如：“按照作业的学科分类”、“从文档、书籍中选择一个关键词”</v-card-subtitle>
          <v-row justify="center" align="center">
            <v-col cols="10">
              <v-text-field v-model="keywordsQuery" variant="underlined"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-spacer></v-spacer>
            <v-col cols="3" align="center">
              <h5>关键词数量</h5>
              <v-number-input v-model="keywordsNumber" :min="1" :max="10" :precision="0"></v-number-input>
            </v-col>
            <v-col cols="1"></v-col>
          </v-row>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.keywords=false;keywordsQuery='';" color="grey"></v-btn>
            <v-btn text="确认" @click="generateKeywords();dialogList.keywords=false;" color="blue" :disabled="keywordsQuery.length==0"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.rm" width="auto">
        <v-card>
          <v-card-title>删除</v-card-title>
          <v-card-text>确定要删除<span v-for="file in selectedFiles" :key="file">"{{file}}"</span>吗？</v-card-text>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.rm=false" color="grey"></v-btn>
            <v-btn text="确认" @click="rm();dialogList.rm=false;" color="blue"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.mkdir" width="400px">
        <v-card>
          <v-card-title>新建文件夹</v-card-title>
          <v-card-text>输入文件夹名称</v-card-text>
          <v-row justify="center">
            <v-col cols="10">
              <v-text-field v-model="newDirName" variant="underlined" :rules="[validateDirName]"></v-text-field>
            </v-col>
          </v-row>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.mkdir=false;newDirname='';" color="grey"></v-btn>
            <v-btn text="确认" @click="mkdir();dialogList.mkdir=false;" color="blue" :disabled="newDirName.length==0"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.paste" width="auto">
        <v-card>
          <v-card-title>粘贴</v-card-title>
          <v-card-text>确定要把<span v-for="dir in fileClipboard.dirs" :key="dir">"{{dir}}"</span>粘贴到此处吗？</v-card-text>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.paste=false" color="grey"></v-btn>
            <v-btn text="确认" @click="paste();dialogList.paste=false;" color="blue"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.fileStat" width="auto">
        <v-card>
          <v-card-title>{{ fileStat.name }}属性</v-card-title>
          <v-list>
            <v-list-item>
              <v-list-item-title>路径</v-list-item-title>
              <v-list-item-subtitle>{{ fileStat.path }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="fileStat.type=='file'">
              <v-list-item-title>大小</v-list-item-title>
              <v-list-item-subtitle>{{ fileStat.size }}字节</v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="fileStat.type=='file'">
              <v-list-item-title>关键词</v-list-item-title>
              <v-list-item-subtitle>
                <span v-for="keyword in fileStat.keywords" :key="keyword">{{ keyword }}&nbsp;</span>
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-btn icon="mdi-pencil" @click="dialogList.modifyKeywords=true" variant="text"></v-btn>
              </template>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>最近访问时间</v-list-item-title>
              <v-list-item-subtitle>{{ Date(fileStat.atime).toLocaleString() }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>最近修改时间</v-list-item-title>
              <v-list-item-subtitle>{{ Date(fileStat.mtime).toLocaleString() }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>ctime(视操作系统而定)</v-list-item-title>
              <v-list-item-subtitle>{{ Date(fileStat.ctime).toLocaleString() }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <template v-slot:actions>
            <v-btn text="确认" @click="dialogList.fileStat=false" color="blue"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.modifyKeywords" width="500px">
        <v-card>
          <v-card-title>关键词列表</v-card-title>
          <v-row justify="center" align="center">
            <v-col cols="10">
              <v-chip
                v-for="(keyword,index) in temporaryKeywords"
                :key="keyword"
                closable
                @click:close="temporaryKeywords.splice(index,1)"
              >{{ keyword }}</v-chip>
            </v-col>
          </v-row>
          <v-row justify="center" align="center">
            <v-col cols="10">
              <v-text-field
                label="添加关键词"
                variant="underlined"
                v-model="newKeyword"
                :rules="[validateKeyword]"
                append-icon="mdi-plus"
                @click:append="addKeyword()"
              ></v-text-field>
            </v-col>
          </v-row>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.modifyKeywords=false" color="grey"></v-btn>
            <v-btn
              text="确认"
              @click="uploadKeywords(fileStat.path,temporaryKeywords).then(()=>ls());dialogList.modifyKeywords=false;"
              color="blue"
              :disabled="temporaryKeywords.length==0"
            ></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogList.moveDirs" width="auto">
        <v-card>
          <v-card-title>更改文件夹结构</v-card-title>
          <v-card-text>是否将文件夹结构更改为：
            <div v-html="generateDirTree(objDirs,0)"></div>
          </v-card-text>
          <template v-slot:actions>
            <v-btn text="取消" @click="dialogList.moveDirs=false" color="grey"></v-btn>
            <v-btn text="确认" @click="moveDirs(objDirs);dialogList.moveDirs=false;" color="blue"></v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-container>
        <v-row>
          <v-col cols="1">
              <v-fab icon>
                <v-icon>{{ isSpeedDialOpen?'mdi-close':'mdi-dots-vertical' }}</v-icon>
                <v-speed-dial
                  v-model="isSpeedDialOpen"
                  transition="slide-y-transition"
                  activator="parent"
                >
                  <v-tooltip text="生成关键词">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-file-export"
                        :disabled="!toolBarInfo.canGenerateKeywords"
                        key="6"
                        @click="dialogList.keywords=true"
                        v-bind="props"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                  <v-tooltip text="新建文件夹">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-folder-plus"
                        key="5"
                        @click="dialogList.mkdir=true"
                        v-bind="props"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                  <v-tooltip text="删除">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-delete"
                        :disabled="!toolBarInfo.canDelete"
                        @click="dialogList.rm=true"
                        key="4"
                        v-bind="props"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                  <v-tooltip text="粘贴">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-content-paste"
                        :disabled="!toolBarInfo.canPaste"
                        key="3"
                        v-bind="props"
                        @click="dialogList.paste=true"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                  <v-tooltip text="剪切">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-content-cut"
                        :disabled="!toolBarInfo.canCut"
                        key="2"
                        v-bind="props"
                        @click="cut()"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                  <v-tooltip text="复制">
                    <template v-slot:activator="{props}">
                      <v-btn
                        size="40"
                        icon="mdi-content-copy"
                        :disabled="!toolBarInfo.canCopy"
                        key="1"
                        v-bind="props"
                        @click="copy()"
                        ></v-btn>
                    </template>
                  </v-tooltip>
                </v-speed-dial>
              </v-fab>
          </v-col>
          <v-col cols="5" align="center" justify="start">
            <v-combobox
              clearable
              v-model="navPath"
              :items="getParentDirs()"
              @change="changePath()"
              @blur="changePath()"
            ></v-combobox>
            <v-list
              lines="one"
              align="start"
              height="500px"
              v-model:selected="selectedFiles"
              select-strategy="leaf"
            >
              <v-list-item v-if="currentPath.lastIndexOf(slash)!=currentPath.length-1">
                <template v-slot:prepend> 
                  <v-icon icon="mdi-arrow-up"></v-icon>
                  <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                  <v-icon icon="mdi-folder-outline"></v-icon>
                </template>
                <v-list-item-title @click="navPath=navPath+slash+'..'+slash;changePath()">..{{ slash }}</v-list-item-title>
              </v-list-item>
              <v-list-item
                v-for="file in dirs"
                :key="file.name"
              >
                <template v-slot:prepend>
                  <v-list-item-action start>
                    <v-checkbox-btn v-model="selectedFiles" :value="file.path" @click="checkToolBar()"></v-checkbox-btn>
                  </v-list-item-action>
                  <v-icon :icon="file.type=='folder'?'mdi-folder-outline':'mdi-file-outline'"></v-icon>
                </template>
                <v-list-item-title @click="navPath=navPath+slash+file.name;changePath()">{{ file.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ file.time }}&nbsp;{{ file.size?(file.size>=0x400?file.size>=0x100000?file.size>=0x40000000?file.size/0x40000000:file.size/0x100000:file.size/0x400:file.size):'' }}{{ file.size?(file.size>=0x400?file.size>=0x100000?file.size>=0x40000000?'GB':'MB':'KB':'B'):'' }}</v-list-item-subtitle>
                <template v-slot:append>
                  <v-btn icon="mdi-dots-horizontal" @click="showStat(file)" variant="text"></v-btn>
                </template>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="6" justify="end">
            <v-card
              height="400px"
              :loading="isChatting"
              class="overflow-auto"
            >
              <v-progress-linear
                v-if="isChatting"
                color="deep-blue"
                height="4"
                indeterminate
              ></v-progress-linear>
              <v-row v-for="(record,index) in chatRecords" :key="index" :justify="record.source=='user'?'end':'start'">
                <v-col cols="10">
                  <v-card :color="record.source=='user'?'blue-lighten-4':'white'">
                    <v-expansion-panels v-if="record.source=='model'" v-model="record.showThought">
                      <v-expansion-panel value="pop">
                        <v-expansion-panel-title>{{ record.showThought=='pop'?'思考中……':record.type=='error'||record.message.match(/^\s*$/)?'已完成部分思考，等待下一步指令':'已完成思考' }}</v-expansion-panel-title>
                        <v-expansion-panel-text>{{ record.thought }}</v-expansion-panel-text>
                      </v-expansion-panel>
                    </v-expansion-panels>
                    <v-chip v-if="record.message.match(/^\{[\s\S]*\}$/)" @click="this.objDirs=JSON.parse(record.message);this.dialogList.moveDirs=true">目录结构</v-chip>
                    <v-card-text v-else>{{ record.message }}</v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
            <v-textarea
              v-model="chatText"
              variant="underlined"
              append-icon="mdi-send"
              @click:append="callLLM()"
            ></v-textarea>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
'use strict';

import { fetchEventSource } from '@microsoft/fetch-event-source';

const controller=new AbortController();
const {signal} =controller;

export default {
  components: {},
  data:()=>({
    fileAPI:'http://192.168.1.3:5000',
    difyAPI:'http://192.168.1.3/v1',
    slash:'\\',
    dirs:[],
    selectedFiles:[],
    filesForKeywords:[],
    currentPath:'D:\\',
    navPath:'',
    newDirName:'',
    chatText:'',
    chatResponse:'',
    chatRecords:[],
    keywordContext:'',
    keywordsQuery:'',
    keywordsNumber:3,
    temporaryKeywords:[],
    newKeyword:'',
    isChatting:false,
    isSpeedDialOpen:false,
    objDirs:JSON.parse('{"path": "D:\\\\分类测试", "directory": [{"type": "folder", "path": "语文", "directory": [{"type": "file", "path": "D:\\\\分类测试\\\\1.txt"}, {"type": "file", "path": "D:\\\\分类测试\\\\4.txt"}]}, {"type": "folder", "path": "数学", "directory": [{"type": "file", "path": "D:\\\\分类测试\\\\2.txt"}, {"type": "file", "path": "D:\\\\分类测试\\\\3.txt"}]}, {"type": "folder", "path": "英语", "directory": [{"type": "file", "path": "D:\\\\分类测试\\\\5.txt"}, {"type": "file", "path": "D:\\\\分类测试\\\\6.txt"}, {"type": "file", "path": "D:\\\\分类测试\\\\7.txt"}]}]}'),
    fileStat:{
      type:'',
      name:'',
      path:'',
      size:'',
      atime:'',
      mtime:'',
      ctime:'',
      keywords:[]
    },
    chatInfo:{
      conversationID:'',
      taskID:''
    },
    toolBarInfo:{
      canCopy:false,
      canCut:false,
      canPaste:false,
      canDelete:false,
      canGenerateKeywords:false
    },
    dialogList:{
      keywords:false,
      mkdir:false,
      rm:false,
      paste:false,
      fileStat:false,
      modifyKeywords:false,
      moveDirs:false
    },
    snackbar:{
      show:false,
      text:''
    },
    fileClipboard:{
      action:'',
      dirs:[]
    }
  }),
  methods:{
    ls(){
      this.$axios({
        method:'get',
        url:this.fileAPI+'/ls',
        params:{
          p:this.currentPath,
          c:0
        },
        responseType:'document'
      })
      .then((response)=>{
        var folders=response.data.getElementsByTagName('folder');
        var files=response.data.getElementsByTagName('file');
        this.dirs=[];
        for(let i=0;i<folders.length;i++){
          this.dirs.push({
            type:'folder',
            name:folders[i].getAttribute('name'),
            path:this.currentPath+this.slash+folders[i].getAttribute('name'),
            time:folders[i].getAttribute('time')
          });
        }
        for(let i=0;i<files.length;i++){
          this.dirs.push({
            type:'file',
            name:files[i].getAttribute('name'),
            path:this.currentPath+this.slash+files[i].getAttribute('name'),
            time:files[i].getAttribute('time'),
            size:files[i].getAttribute('size'),
            keywords:files[i].getAttribute('keywords')
          });
        }
        for(let i=0;i<this.dirs.length;i++){
          this.dirs[i].path=this.dirs[i].path.replace(this.slash+this.slash,this.slash);
        }
      })
      .catch(function(error){
        console.log(error);
      });
    },
    async cd(path=''){
      var flag=0;
      flag=await this.$axios({
        method:'get',
        url:this.fileAPI+'/cd',
        params:{
          p:path
        },
      })
      .then((response)=>{
        if(response.data){
          this.currentPath=response.data;
          flag=1;
          this.checkToolBar();
        }
        return flag;
      });
      return flag;
    },
    async rm(){
      for(let file in this.selectedFiles){
        this.$axios({
          method:'get',
          url:this.fileAPI+'/rm',
          params:{
            p:this.selectedFiles[file]
          }
        })
        .then((response)=>{
          if(response.data=="Done."){
            if(file==this.selectedFiles.length-1){
              this.selectedFiles=[];
              this.ls();
              this.showSnackbar('Done.');
            }
          }
          else{
            this.showSnackbar(response.data);
          }
        })
      }
    },
    async mkdir(){
      if(this.validateDirName(this.newDirName)===true){
        this.currentPath=(this.currentPath+this.slash+this.newDirName).replace(this.slash+this.slash,this.slash)
        this.$axios({
          method:'get',
          url:this.fileAPI+'/mkdir',
          params:{
            p:this.currentPath
          }
        })
        .then((response)=>{
          console.log(response);
          this.cd(this.currentPath);
          this.navPath=this.currentPath;
          this.ls();
          this.showSnackbar('Done.')
        });
      }
      else{
        this.showSnackbar('名称含有非法字符');
      }
    },
    validateDirName(name){
      if(name.match(/([<>:"/\\|?*]|CON|PRN|AUX|NUL|COM\d|LPT\d)+/)){
        return '文件夹名称含有非法字符';
      }
      else{
        return true;
      }
    },
    async copy(){
      this.fileClipboard.action='copy';
      this.fileClipboard.dirs=this.selectedFiles;
      console.log(this.fileClipboard);
      this.checkToolBar();
    },
    async cut(){
      this.fileClipboard.action='cut';
      this.fileClipboard.dirs=this.selectedFiles;
      console.log(this.fileClipboard);
      this.checkToolBar();
    },
    async paste(){
      if(this.fileClipboard.action=='copy'){
        for(let dir in this.fileClipboard.dirs){
          await this.$axios({
            method:'get',
            url:this.fileAPI+'/copy',
            params:{
              s:this.fileClipboard.dirs[dir],
              d:(this.currentPath+this.slash+this.fileClipboard.dirs[dir].split(this.slash).pop()).replace(this.slash+this.slash,this.slash)
            }
          })
          .then((response)=>{
            console.log(response.data);
          });
        }
      }
      else{
        if(this.fileClipboard.action=='cut'){
          for(let dir in this.fileClipboard.dirs){
          await this.$axios({
            method:'get',
            url:this.fileAPI+'/cut',
            params:{
              s:this.fileClipboard.dirs[dir],
              d:(this.currentPath+this.slash+this.fileClipboard.dirs[dir].split(this.slash).pop()).replace(this.slash+this.slash,this.slash)
            }
          })
          .then((response)=>{
            console.log(response.data);
          });
        }
        }
      }
      this.ls();
    },
    async changePath(){
      if(await this.cd(this.navPath)){
        this.currentPath=this.currentPath.replace(this.slash+this.slash,this.slash);
        this.ls();
        this.selectedFiles=[];
      }
      this.navPath=this.currentPath;
      this.checkToolBar();
    },
    getParentDirs(){
      var s=this.currentPath.split(this.slash);
      var p=[s[0]];
      for(let i=1;i<s.length;i++){
        if(s[i])
          p[i]=p[i-1]+this.slash+s[i];
      }
      p[0]=p[0]+this.slash;
      return p;
    },
    async callLLM(){
      var d;
      var lastMessage='';
      this.chatRecords.push({
        source:'user',
        message:this.chatText
      });
      var index=this.chatRecords.length;
      fetchEventSource(this.difyAPI+'/chat-messages',{
        method:'POST',
        headers:{
          'Authorization':'Bearer app-VeSEBbcHrFP0SpYIeaJqWMmf',
          'Content-Type':'application/json'
        },
        body:JSON.stringify({
          inputs:{},
          response_mode:'streaming',
          conversation_id:this.chatInfo.conversationID,
          query:JSON.stringify({
            action:'chat',
            data:this.chatText
          }),
          user:'test_user',
          files:[]
        }),
        signal,
        onopen:(response)=>{
          console.log(response.status);
          this.chatText='';
          if(response.status==200){
            this.chatRecords.push({
              source:'model',
              thought:'',
              message:'',
              showThought:'pop',
              type:'thinking'
            });
            console.log(this.chatRecords);
          }
        },
        onmessage:(event)=>{
          if(event.event=='ping'){
            console.log('ping');
          }
          else{
            d=JSON.parse(event.data);
            if(this.chatInfo.conversationID==''){
              this.chatInfo.conversationID=d.conversation_id;
              this.chatInfo.taskID=d.task_id;
            }
            if(d.event=='agent_message'){
              this.chatRecords[index].thought=this.chatResponse;
              this.chatResponse=this.chatResponse+d.answer;
              lastMessage=d.answer;
            }
            else{
              if(d.event=='message_end'){
                this.isChatting=false;
                this.chatRecords[index].message=lastMessage;
                this.chatRecords[index].showThought=null;
                this.chatRecords[index].type='answer';
                console.log(this.chatRecords);
                console.log(this.chatRecords[index].message.match(/^\{\S*\}$/));
                for(let r in this.chatRecords){
                  if(!this.chatRecords[r].thought&&this.chatRecords.source=='model'){
                    this.chatRecords.splice(r,1);
                  }
                }
                controller.abort();
              }
              else{
                if(d.event=='error'){
                  this.isChatting=false;
                  this.chatRecords[index].showThought=null;
                  this.chatRecords[index].type='error';
                  console.log(this.chatRecords);
                  controller.abort();
                }
              }
            }
          }
        },
        onerror:(err)=>{
          console.error(err);
          console.log(d);
          controller.abort();
        },
        onclose:()=>{
          this.isChatting=false;
        }
      });
    },
    async getKeywords(file,description,n){
      this.keywordContext='';
      var path=this.filesForKeywords[file].path;
      var fileText='';
      var taskID='';
      var lastMessage='';
      var d={};
      var e={};
      await this.$axios({
        method:'get',
        url:this.fileAPI+'/get-text',
        params:{
          p:path
        }
      })
      .then((response)=>{
        fileText=response.data;
      });
      return fetchEventSource(this.difyAPI+'/chat-messages',{
        method:'POST',
        headers:{
          'Authorization':'Bearer app-VeSEBbcHrFP0SpYIeaJqWMmf',
          'Content-Type':'application/json'
        },
        body:JSON.stringify({
          inputs:{},
          response_mode:'streaming',
          conversation_id:this.conversationID,
          query:JSON.stringify({
            action:'keywords',
            data:fileText,
            description:description,
            number:n
          }),
          user:'test_user',
          files:[]
        }),
        signal,
        onmessage:(event)=>{
          if(event.event=='ping'){
            console.log('ping');
          }
          else{
            d=JSON.parse(event.data);
            if(d.event=='agent_message'){
              if(taskID==''){
                taskID=d.task_id;
              }
              this.chatRecords
              this.keywordContext=this.keywordContext+d.answer;
              lastMessage=d.answer;
            }
            else{
              if(d.event=='message_end'){
                console.log(this.keywordContext);
                this.filesForKeywords[file].stat=true;
                this.filesForKeywords[file].keywords=JSON.parse(lastMessage).keywords;
                console.log(this.filesForKeywords);
                controller.abort();
              }
            }
          }
        },
        onerror:(err)=>{
          console.log(err);
          console.log(this.keywordContext);
          console.log(e)
          controller.abort();
        }
      });
    },
    async stopLLM(taskID){
      this.$axios({
        method:'post',
        url:this.difyAPI+'/chat-messages/:'+taskID+'/stop',
        headers:{
          'Authorization':'Bearer app-VeSEBbcHrFP0SpYIeaJqWMmf',
          'Content-Type':'application/json'
        },
        data:{
          user:"test_user"
        }
      })
      .then((response)=>{
        console.log(response.data);
      })
      .finally(()=>{
        this.isChatting=false;
      });
    },
    async checkToolBar(){
      setTimeout(()=>{
        if(this.selectedFiles.length>=1){
          this.toolBarInfo.canCopy=true;
          this.toolBarInfo.canCut=true;
          this.toolBarInfo.canDelete=true;
          this.toolBarInfo.canGenerateKeywords=true;
          for(let file in this.dirs){
            for(let n in this.selectedFiles){
              if(this.dirs[file].path==this.selectedFiles[n]&&this.dirs[file].type=='folder'){
                this.toolBarInfo.canGenerateKeywords=false;
                break;
              }
            }
          }
        }
        else{
          this.toolBarInfo.canCopy=false;
          this.toolBarInfo.canCut=false;
          this.toolBarInfo.canDelete=false;
          this.toolBarInfo.canGenerateKeywords=false;
        }
        if(this.fileClipboard.dirs.length===0){
          this.toolBarInfo.canPaste=false;
        }
        else{
          this.toolBarInfo.canPaste=true;
        }
        if(this.toolBarInfo.canCopy||this.toolBarInfo.canCut||this.toolBarInfo.canPaste||this.toolBarInfo.canDelete||this.toolBarInfo.canGenerateKeywords){
          this.isSpeedDialOpen=true;
        }
      },100);
    },
    async uploadKeywords(path,keywords){
      return this.$axios({
        method:'post',
        url:this.fileAPI+'/store-keywords',
        params:{
          p:path
        },
        data:{
          keywords:keywords
        }
      })
      .then((response)=>{
        console.log(response.data);
      });
    },
    async generateKeywords(){
      var query=this.keywordsQuery;
      this.keywordsQuery='';
      this.filesForKeywords=[];
      for(let file in this.selectedFiles){
        this.filesForKeywords.push({
          path:this.selectedFiles[file],
          stat:false,
          keywords:[]
        })
      }
      console.log(this.currentPath);
      console.log(this.selectedFiles);
      console.log(this.filesForKeywords);
      for(let file in this.filesForKeywords){
        await this.getKeywords(file,query,this.keywordsNumber);
        if(this.filesForKeywords[file].stat){
          this.showSnackbar('关键词已生成('+(Number(file)+1)+'/'+this.filesForKeywords.length+')');
          this.uploadKeywords(this.filesForKeywords[file].path,this.filesForKeywords[file].keywords);
        }
      }
      this.ls();
    },
    validateKeyword(keyword){
      if(keyword.match(/\s/)){
        return '关键词不可含有空白字符';
      }
      else{
        return true;
      }
    },
    addKeyword(){
      if(this.validateKeyword(this.newKeyword)===true){
        this.temporaryKeywords.push(this.newKeyword);
        this.newKeyword='';
      }
      else{
        this.showSnackbar('关键词不能含有空白字符');
      }
    },
    showStat(file){
      this.fileStat.type=file.type;
      this.fileStat.name=file.name;
      this.fileStat.path=file.path;
      if(file.keywords){
        this.fileStat.keywords=file.keywords.split(' ');
      }
      else{
        this.fileStat.keywords=[];
      }
      this.temporaryKeywords=this.fileStat.keywords;
      this.$axios({
        method:'get',
        url:this.fileAPI+'/stat',
        params:{
          p:file.path
        }
      })
      .then((response)=>{
        let stat=response.data;
        this.fileStat.size=stat[6];
        this.fileStat.atime=stat[7];
        this.fileStat.mtime=stat[8];
        this.fileStat.ctime=stat[9];
        this.dialogList.fileStat=true;
      })
    },
    showSnackbar(text){
      this.snackbar.text=text;
      this.snackbar.show=true;
      setTimeout(()=>{
        this.snackbar.show=false;
        this.snackbar.text='';
      },2000);
    },
    generateDirTree(dir,depth){
      var indent='';
      for(let i=0;i<depth;i++){
        indent=indent+'&nbsp;&nbsp;';
      }
      var str=indent+dir.path;
      indent=indent+'&nbsp;&nbsp;';
      for(let d in dir.directory){
        if(dir.directory[d].type=='folder'){
          str=str+'<br>'+this.generateDirTree(dir.directory[d],depth+1);
        }
        else{
          if(dir.directory[d].type=='file'){
            str=str+'<br>'+indent+dir.directory[d].path;
          }
        }
      }
      return str;
    },
    async moveDirs(tree){
      var cp=this.currentPath;
      await this.cd(tree.path);
      for(let dir in tree.directory){
        if(tree.directory[dir].type=='folder'){
          tree.directory[dir].path=tree.path+this.slash+tree.directory[dir].path;
          await this.$axios({
            method:'get',
            url:this.fileAPI+'/mkdir',
            params:{
              p:tree.directory[dir].path
            }
          })
          .then((response)=>{
            console.log(response);
          });
          await this.moveDirs(tree.directory[dir]);
        }
        else{
          if(tree.directory[dir].type=='file'){
            await this.$axios({
              method:'get',
              url:this.fileAPI+'/cut',
              params:{
                s:tree.directory[dir].path,
                d:this.currentPath+this.slash+tree.directory[dir].path.split(this.slash).pop()
              }
            })
            .then((response)=>{
              console.log(response.data);
            });
          }
        }
      }
      if(!tree.type){
        await this.cd(cp);
        this.ls();
      }
    }
  },
  created(){
    this.navPath=this.currentPath;
    this.ls();
    this.cd(this.currentPath);
  }
}
</script>