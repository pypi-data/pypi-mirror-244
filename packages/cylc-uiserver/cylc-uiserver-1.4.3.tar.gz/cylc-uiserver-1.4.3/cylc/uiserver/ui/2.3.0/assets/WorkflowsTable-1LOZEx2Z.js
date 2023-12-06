import{bz as u,c7 as f,e6 as k,c8 as b,e7 as p,cg as h,ch as _,ci as m,e8 as r,cb as g,aM as w,aN as W,o as y,bs as l,bC as v,az as C,z as a,bD as T,r as e,a_ as t,bu as $,bE as D}from"./index-p5QwxXYb.js";import{V as N}from"./VAlert-euxRuCvE.js";const V=f`
subscription Workflow {
  deltas {
    id
    added {
      workflow {
        ...WorkflowData
      }
    }
    updated (stripNull: true) {
      workflow {
        ...WorkflowData
      }
    }
    pruned {
      workflow
    }
  }
}

fragment WorkflowData on Workflow {
  id
  status
  owner
  host
  port
}
`,x={name:"WorkflowsTable",mixins:[k],head(){return{title:b("App.workflows")}},components:{WorkflowIcon:p},data:()=>({query:new h(V,{},"root",[],!0,!0)}),computed:{..._("workflows",["cylcTree"]),...m("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(s){this.$router.push({path:`/workspace/${s.tokens.workflow}`})}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:r.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:r.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:r.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:r.global.t("Workflows.tableColumnPort"),key:"node.port"}],icons:{mdiTable:g}},S={class:"text-h5"},j=["onClick"],z={width:"1em"};function B(s,I,q,A,E,n){const i=w("WorkflowIcon"),c=w("v-data-table"),d=W("cylc-object");return C(),y(v,{"fill-height":"",fluid:"","grid-list-xl":""},{default:l(()=>[a(D,{class:"align-self-start"},{default:l(()=>[a(T,null,{default:l(()=>[a(N,{icon:s.$options.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:l(()=>[e("h3",S,t(s.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),a(c,{headers:s.$options.headers,items:n.workflowsTable,"data-cy":"workflows-table"},{item:l(({item:o})=>[e("tr",{onClick:H=>n.viewWorkflow(o.raw),style:{cursor:"pointer"}},[e("td",z,[$(a(i,{status:o.raw.node.status},null,8,["status"]),[[d,o.raw]])]),e("td",null,t(o.raw.tokens.workflow),1),e("td",null,t(o.raw.node.status),1),e("td",null,t(o.raw.node.owner),1),e("td",null,t(o.raw.node.host),1),e("td",null,t(o.raw.node.port),1)],8,j)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const P=u(x,[["render",B]]);export{P as default};
