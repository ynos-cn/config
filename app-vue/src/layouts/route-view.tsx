import { defineComponent, KeepAlive as VKeepAlive, h, Component } from 'vue'
import { RouterView, useRoute } from 'vue-router'

const RouteView = defineComponent({
  name: 'RouteView',
  props: {
    keepAlive: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const route = useRoute()

    const inKeep = () => {
      return (
        <RouterView
          v-slots={{
            default: ({ Component }: { Component: Component }) => {
              return (
                <VKeepAlive
                  v-slots={{
                    default: () => {
                      return h(Component)
                    }
                  }}
                />
              )
            }
          }}
        />
      )
    }

    const notKeep = () => {
      return <RouterView />
    }

    return () => {
      return route.meta.keepAlive || props.keepAlive ? inKeep() : notKeep()
    }
  }
})

export default RouteView
