<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>增加商品</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-alert title="增加商品信息" type="info" center show-icon></el-alert>

      <el-steps :active="active-0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="商品静态参数"></el-step>
        <el-step title="商品动态参数"></el-step>
        <el-step title="商品图片"></el-step>
        <el-step title="商品内容"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>

      <el-form :model="addForm" ref="addRef" :rules="addRules" label-position="top">
        <el-tabs v-model="active" :tab-position="'left'" :before-leave="beforeLeave">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" prop="name">
              <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" prop="price">
              <el-input v-model="addForm.price"></el-input>
            </el-form-item>
            <el-form-item label="商品数量" prop="number">
              <el-input v-model="addForm.number"></el-input>
            </el-form-item>
            <el-form-item label="商品权重" prop="weight">
              <el-input v-model="addForm.weight"></el-input>
            </el-form-item>
            <el-form-item label="商品分类" prop="cid">
              <el-cascader
                v-model="selectKeys"
                :options="cateIdList"
                :props="{ expandTrigger: 'hover', label:'name', value:'id'}"
                clearable
                separator=" > "
                @change="changeSeletor"
              ></el-cascader>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品静态参数" name="1">
            <el-form-item :label="s.name" v-for="s in attr_static" :key="s.id">
              <el-input v-model="s.val"></el-input>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品动态参数" name="2">
            <el-form-item :label="d.name" v-for="d in attr_dynamic" :key="d.id">
              <el-checkbox-group v-model="d.val">
                <el-checkbox :label="dv" v-for="(dv,i) in d.val" :key="i" border></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品图片" name="3">
            <el-upload
              class="upload-demo"
              action="/upload_img"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-success="handleSuccess"
              list-type="picture"
            >
              <el-button size="small" type="primary">点击上传</el-button>
            </el-upload>
          </el-tab-pane>
          <el-tab-pane label="商品内容" name="4">
            <quill-editor v-model="addForm.introduce"></quill-editor>
            <el-button type="primary" @click="goodsAdd" class="btnAdd">添加商品</el-button>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
    <el-dialog title="图片预览" :visible.sync="previewVisible" width="40%">
      <img :src="previewPath" class="preImg" />
    </el-dialog>
  </div>
</template>
<script>
export default {
  data() {
    return {
      active: '0',
      addForm: {
        name: '',
        price: 0,
        number: 0,
        weight: 0,
        cid_one: 0,
        cid_two: 0,
        cid_three: 0,
        pics: [],
        introduce: '',
        attr_static: [],
        attr_dynamic: []
      },
      addRules: {
        name: [{ required: true, message: '请输填写商品名称', tigger: 'blur' }],
        price: [
          { required: true, message: '请输填写商品价格', tigger: 'blur' }
        ],
        number: [
          { required: true, message: '请输填写商品数量', tigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输填写商品权重', tigger: 'blur' }
        ]
      },
      cateIdList: [],
      selectKeys: [],
      attr_static: [],
      attr_dynamic: [],
      previewVisible: false,
      previewPath: ''
    }
  },
  created() {
    this.getCateIDList()
  },
  methods: {
    async getCateIDList() {
      const { data: resp } = await this.$axios.get('/category_list')
      this.cateIdList = resp.data.data
    },
    changeSeletor() {
      if (this.selectKeys.length < 3) return
      this.addForm.cid_one = this.selectKeys[0]
      this.addForm.cid_two = this.selectKeys[1]
      this.addForm.cid_three = this.selectKeys[2]
      console.log(this.addForm)
    },
    beforeLeave(activeName, oldActiveName) {
      if (this.selectKeys.length < 3) {
        this.$msg.error('请求选择商品分类！！')
        return false
      }
      if (activeName === '1') this.getAttribute('static')
      if (activeName === '2') this.getAttribute('dynamic')
    },
    async getAttribute(_type) {
      const { data: resp } = await this.$axios.get('/category/attr_list', {
        params: { cid: this.selectKeys[2], _type: _type }
      })
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      if (_type === 'static') {
        this.attr_static = resp.data
      } else {
        resp.data.forEach(item => {
          item.val = item.val ? item.val.split(',') : []
        })
        this.attr_dynamic = resp.data
      }
    },
    handleSuccess(resp) {
      this.addForm.pics.push(resp.data.path)
    },
    handleRemove(file) {
      // console.log(file)
      // console.log(this.addForm.pics)
      const i = this.addForm.pics.findIndex(x => x === file.response.data.path)
      this.addForm.pics.splice(i, 1)
      // console.log(this.addForm.pics)
    },
    handlePreview(file) {
      // console.log(file)
      this.previewVisible = true
      this.previewPath = file.response.data.url
    },
    goodsAdd() {
      this.$refs.addRef.validate(async valid => {
        if (!valid) return this.$msg.error('请填写必要的参数！！')
      })
      const staticList = []
      this.attr_static.forEach(atr => {
        staticList.push({ id: atr.id, val: atr.val })
      })
      this.addForm.attr_static = JSON.stringify(staticList)
      const dynamicList = []
      this.attr_dynamic.forEach(atr => {
        dynamicList.push({ id: atr.id, val: atr.val.join(',') })
      })
      this.addForm.attr_dynamic = JSON.stringify(dynamicList)
      this.addForm.pics = JSON.stringify(this.addForm.pics)

      // console.log(this.addForm)
      this.saveGoods()
    },
    async saveGoods() {
      const { data: resp } = await this.$axios.post(
        '/goods',
        this.$qs.stringify(this.addForm)
      )
      if (resp.status !== 200) return this.$msg.error(resp.msg)
      this.$msg.success(resp.msg)
      this.$router.push('/goods_list')
    }
  }
}
</script>
<style lang="less" scoped>
.el-tabs {
  margin-top: 10px;
}
.el-alert {
  margin-bottom: 10px;
}
.el-cascader {
  width: 500px;
}
.el-checkbox {
  margin: 0 10px 0 0 !important;
}
.preImg {
  width: 100%;
}
.btnAdd {
  margin-top: 10px;
}
</style>