## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">Find ${model_title_plural} by Permission</%def>

<%def name="page_content()">
  <br />
  <find-principals :permission-groups="permissionGroups"
                   :sorted-groups="sortedGroups">
  </find-principals>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  <script type="text/x-template" id="find-principals-template">
    <div>

      ${h.form(request.current_route_url(), method='GET', **{'@submit': 'formSubmitting = true'})}
        <div style="margin-left: 10rem; max-width: 50%;">

          ${h.hidden('permission_group', **{':value': 'selectedGroup'})}
          <b-field label="Permission Group" horizontal>
            <b-autocomplete v-if="!selectedGroup"
                            ref="permissionGroupAutocomplete"
                            v-model="permissionGroupTerm"
                            :data="permissionGroupChoices"
                            field="groupkey"
                            :custom-formatter="filtr => filtr.label"
                            open-on-focus
                            keep-first
                            icon-pack="fas"
                            clearable
                            clear-on-select
                            @select="permissionGroupSelect">
            </b-autocomplete>
            <b-button v-if="selectedGroup"
                      @click="permissionGroupReset()">
              {{ permissionGroups[selectedGroup].label }}
            </b-button>
          </b-field>

          ${h.hidden('permission', **{':value': 'selectedPermission'})}
          <b-field label="Permission" horizontal>
            <b-autocomplete v-if="!selectedPermission"
                            ref="permissionAutocomplete"
                            v-model="permissionTerm"
                            :data="permissionChoices"
                            field="permkey"
                            :custom-formatter="filtr => filtr.label"
                            open-on-focus
                            keep-first
                            icon-pack="fas"
                            clearable
                            clear-on-select
                            @select="permissionSelect">
            </b-autocomplete>
            <b-button v-if="selectedPermission"
                      @click="permissionReset()">
              {{ selectedPermissionLabel }}
            </b-button>
          </b-field>

          <b-field horizontal>
            <div class="buttons" style="margin-top: 1rem;">
              <once-button tag="a"
                           href="${request.current_route_url(_query=None)}"
                           text="Reset Form">
              </once-button>
              <b-button type="is-primary"
                        native-type="submit"
                        icon-pack="fas"
                        icon-left="search"
                        :disabled="formSubmitting">
                {{ formSubmitting ? "Working, please wait..." : "Find ${model_title_plural}" }}
              </b-button>
            </div>
          </b-field>

        </div>
      ${h.end_form()}

      % if principals is not None:
      <div class="grid half">
        <br />
        <h2>Found ${len(principals)} ${model_title_plural} with permission: ${selected_permission}</h2>
        ${self.principal_table()}
      </div>
      % endif

    </div>
  </script>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.permissionGroups = ${json.dumps(buefy_perms)|n}
    ThisPageData.sortedGroups = ${json.dumps(buefy_sorted_groups)|n}

  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    Vue.component('find-principals', {
        template: '#find-principals-template',
        props: {
            permissionGroups: Object,
            sortedGroups: Array
        },
        data() {
            return {
                groupPermissions: ${json.dumps(buefy_perms.get(selected_group, {}).get('permissions', []))|n},
                permissionGroupTerm: '',
                permissionTerm: '',
                selectedGroup: ${json.dumps(selected_group)|n},
                selectedPermission: ${json.dumps(selected_permission)|n},
                selectedPermissionLabel: ${json.dumps(selected_permission_label or '')|n},
                formSubmitting: false,
            }
        },

        computed: {

            permissionGroupChoices() {

                // collect all groups
                let choices = []
                for (let groupkey of this.sortedGroups) {
                    choices.push(this.permissionGroups[groupkey])
                }

                // parse list of search terms
                let terms = []
                for (let term of this.permissionGroupTerm.toLowerCase().split(' ')) {
                    term = term.trim()
                    if (term) {
                        terms.push(term)
                    }
                }

                // filter groups by search terms
                choices = choices.filter(option => {
                    let label = option.label.toLowerCase()
                    for (let term of terms) {
                        if (label.indexOf(term) < 0) {
                            return false
                        }
                    }
                    return true
                })

                return choices
            },

            permissionChoices() {

                // collect all permissions for current group
                let choices = this.groupPermissions

                // parse list of search terms
                let terms = []
                for (let term of this.permissionTerm.toLowerCase().split(' ')) {
                    term = term.trim()
                    if (term) {
                        terms.push(term)
                    }
                }

                // filter permissions by search terms
                choices = choices.filter(option => {
                    let label = option.label.toLowerCase()
                    for (let term of terms) {
                        if (label.indexOf(term) < 0) {
                            return false
                        }
                    }
                    return true
                })

                return choices
            },
        },

        methods: {

            permissionGroupSelect(option) {
                this.selectedPermission = null
                this.selectedPermissionLabel = null
                if (option) {
                    this.selectedGroup = option.groupkey
                    this.groupPermissions = this.permissionGroups[option.groupkey].permissions
                    this.$nextTick(() => {
                        this.$refs.permissionAutocomplete.focus()
                    })
                }
            },

            permissionGroupReset() {
                this.selectedGroup = null
                this.selectedPermission = null
                this.selectedPermissionLabel = ''
                this.$nextTick(() => {
                    this.$refs.permissionGroupAutocomplete.focus()
                })
            },

            permissionSelect(option) {
                if (option) {
                    this.selectedPermission = option.permkey
                    this.selectedPermissionLabel = option.label
                }
            },

            permissionReset() {
                this.selectedPermission = null
                this.selectedPermissionLabel = null
                this.permissionTerm = ''
                this.$nextTick(() => {
                    this.$refs.permissionAutocomplete.focus()
                })
            },
        }
    })

  </script>
</%def>


${parent.body()}
