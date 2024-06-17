if(CONFIG_BT_ENABLED)
    set(srcs "")
    set(include_dirs "")
    set(priv_include_dirs
            common/btc/include
            common/include
            porting/mem
        )

    if(NOT (CONFIG_BT_LE_CRYPTO_STACK_MBEDTLS OR CONFIG_BT_NIMBLE_CRYPTO_STACK_MBEDTLS))
        list(APPEND include_dirs
                ext/tinycrypt/include
            )
        list(APPEND srcs "ext/tinycrypt/src/utils.c"
                "ext/tinycrypt/src/sha256.c"
                "ext/tinycrypt/src/ecc.c"
                "ext/tinycrypt/src/ctr_prng.c"
                "ext/tinycrypt/src/ctr_mode.c"
                "ext/tinycrypt/src/aes_decrypt.c"
                "ext/tinycrypt/src/aes_encrypt.c"
                "ext/tinycrypt/src/ccm_mode.c"
                "ext/tinycrypt/src/ecc_dsa.c"
                "ext/tinycrypt/src/cmac_mode.c"
                "ext/tinycrypt/src/ecc_dh.c"
                "ext/tinycrypt/src/hmac_prng.c"
                "ext/tinycrypt/src/ecc_platform_specific.c"
                "ext/tinycrypt/src/hmac.c"
                "ext/tinycrypt/src/cbc_mode.c")
    endif()

    list(APPEND include_dirs
                nimble/host/include
                nimble/include
                nimble/host/services/ans/include
                nimble/host/services/bas/include
                nimble/host/services/dis/include
                nimble/host/services/gap/include
                nimble/host/services/gatt/include
                nimble/host/services/hr/include
                nimble/host/services/htp/include
                nimble/host/services/ias/include
                nimble/host/services/ipss/include
                nimble/host/services/lls/include
                nimble/host/services/prox/include
                nimble/host/services/cts/include
                nimble/host/services/tps/include
                nimble/host/services/hid/include
                nimble/host/services/sps/include
                nimble/host/util/include
                nimble/host/store/ram/include
                nimble/host/store/config/include
                esp-hci/include
                )

    list(APPEND srcs "nimble/transport/src/transport.c"
                "nimble/host/util/src/addr.c"
                "nimble/host/services/gatt/src/ble_svc_gatt.c"
                "nimble/host/services/tps/src/ble_svc_tps.c"
                "nimble/host/services/ias/src/ble_svc_ias.c"
                "nimble/host/services/ipss/src/ble_svc_ipss.c"
                "nimble/host/services/ans/src/ble_svc_ans.c"
                "nimble/host/services/hr/src/ble_svc_hr.c"
                "nimble/host/services/htp/src/ble_svc_htp.c"
                "nimble/host/services/gap/src/ble_svc_gap.c"
                "nimble/host/services/bas/src/ble_svc_bas.c"
                "nimble/host/services/dis/src/ble_svc_dis.c"
                "nimble/host/services/lls/src/ble_svc_lls.c"
                "nimble/host/services/prox/src/ble_svc_prox.c"
                "nimble/host/services/cts/src/ble_svc_cts.c"
                "nimble/host/services/hid/src/ble_svc_hid.c"
                "nimble/host/services/sps/src/ble_svc_sps.c"
                "nimble/host/src/ble_hs_conn.c"
                "nimble/host/src/ble_store_util.c"
                "nimble/host/src/ble_sm.c"
                "nimble/host/src/ble_hs_shutdown.c"
                "nimble/host/src/ble_l2cap_sig_cmd.c"
                "nimble/host/src/ble_hs_hci_cmd.c"
                "nimble/host/src/ble_hs_id.c"
                "nimble/host/src/ble_att_svr.c"
                "nimble/host/src/ble_gatts_lcl.c"
                "nimble/host/src/ble_ibeacon.c"
                "nimble/host/src/ble_hs_atomic.c"
                "nimble/host/src/ble_sm_alg.c"
                "nimble/host/src/ble_hs_stop.c"
                "nimble/host/src/ble_hs.c"
                "nimble/host/src/ble_hs_hci_evt.c"
                "nimble/host/src/ble_hs_mqueue.c"
                "nimble/host/src/ble_hs_periodic_sync.c"
                "nimble/host/src/ble_att.c"
                "nimble/host/src/ble_ead.c"
                "nimble/host/src/ble_aes_ccm.c"
                "nimble/host/src/ble_gattc.c"
                "nimble/host/src/ble_store.c"
                "nimble/host/src/ble_sm_lgcy.c"
                "nimble/host/src/ble_hs_cfg.c"
                "nimble/host/src/ble_att_clt.c"
                "nimble/host/src/ble_l2cap_coc.c"
                "nimble/host/src/ble_hs_mbuf.c"
                "nimble/host/src/ble_att_cmd.c"
                "nimble/host/src/ble_hs_log.c"
                "nimble/host/src/ble_eddystone.c"
                "nimble/host/src/ble_hs_startup.c"
                "nimble/host/src/ble_l2cap_sig.c"
                "nimble/host/src/ble_gap.c"
                "nimble/host/src/ble_sm_cmd.c"
                "nimble/host/src/ble_uuid.c"
                "nimble/host/src/ble_hs_pvcy.c"
                "nimble/host/src/ble_hs_flow.c"
                "nimble/host/src/ble_l2cap.c"
                "nimble/host/src/ble_sm_sc.c"
                "nimble/host/src/ble_hs_misc.c"
                "nimble/host/src/ble_gatts.c"
                "nimble/host/src/ble_hs_adv.c"
                "nimble/host/src/ble_hs_hci.c"
                "nimble/host/src/ble_hs_hci_util.c"
                "nimble/host/src/ble_hs_resolv.c"
                "nimble/host/store/ram/src/ble_store_ram.c"
                "nimble/host/store/config/src/ble_store_config.c"
                "nimble/host/store/config/src/ble_store_nvs.c"
                "nimble/host/src/ble_gattc_cache.c"
                "nimble/host/src/ble_gattc_cache_conn.c"
                "esp-hci/src/esp_nimble_hci.c"
            )

        list(APPEND srcs
            "porting/nimble/src/nimble_port.c"
            "porting/npl/freertos/src/nimble_port_freertos.c"
            "port/src/nvs_port.c"
        )

        list(APPEND include_dirs
            porting/include
            porting/nimble/include
            port/include
            nimble/transport/include
        )

    if(NOT CONFIG_BT_LE_CONTROLLER_NPL_OS_PORTING_SUPPORT)
        list(APPEND srcs
                "porting/nimble/src/endian.c"
                "porting/nimble/src/os_mempool.c"
                "porting/nimble/src/mem.c"
                "porting/nimble/src/os_mbuf.c"
                "porting/nimble/src/os_msys_init.c"
                "porting/npl/freertos/src/npl_os_freertos.c"
                )

        list(APPEND include_dirs
                porting/npl/freertos/include
                porting/nimble/include
                nimble/include
        )
    endif()

    if(CONFIG_BT_NIMBLE_MESH)

        list(APPEND include_dirs
            nimble/host/mesh/include
            nimble/host/include/host)

        list(APPEND srcs "nimble/host/mesh/src/shell.c"
                    "nimble/host/mesh/src/friend.c"
                    "nimble/host/mesh/src/crypto.c"
                    "nimble/host/mesh/src/settings.c"
                    "nimble/host/mesh/src/adv.c"
                    "nimble/host/mesh/src/adv_ext.c"
                    "nimble/host/mesh/src/adv_legacy.c"
                    "nimble/host/mesh/src/model_srv.c"
                    "nimble/host/mesh/src/msg.c"
                    "nimble/host/mesh/src/beacon.c"
                    "nimble/host/mesh/src/glue.c"
                    "nimble/host/mesh/src/model_cli.c"
                    "nimble/host/mesh/src/transport.c"
                    "nimble/host/mesh/src/prov.c"
                    "nimble/host/mesh/src/mesh.c"
                    "nimble/host/mesh/src/access.c"
                    "nimble/host/mesh/src/cfg_srv.c"
                    "nimble/host/mesh/src/cfg_cli.c"
                    "nimble/host/mesh/src/light_model.c"
                    "nimble/host/mesh/src/health_cli.c"
                    "nimble/host/mesh/src/lpn.c"
                    "nimble/host/mesh/src/health_srv.c"
                    "nimble/host/mesh/src/testing.c"
                    "nimble/host/mesh/src/aes-ccm.c"
                    "nimble/host/mesh/src/app_keys.c"
                    "nimble/host/mesh/src/cdb.c"
                    "nimble/host/mesh/src/cfg.c"
                    "nimble/host/mesh/src/pb_adv.c"
                    "nimble/host/mesh/src/pb_gatt.c"
                    "nimble/host/mesh/src/pb_gatt_srv.c"
                    "nimble/host/mesh/src/prov_device.c"
                    "nimble/host/mesh/src/provisioner.c"
                    "nimble/host/mesh/src/heartbeat.c"
                    "nimble/host/mesh/src/rpl.c"
                    "nimble/host/mesh/src/subnet.c"
                    "nimble/host/mesh/src/proxy_msg.c"
                    "nimble/host/mesh/src/proxy_srv.c"
                    "nimble/host/mesh/src/net.c")
    endif()

endif()

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS "${include_dirs}"
                       PRIV_INCLUDE_DIRS "${priv_include_dirs}"
                       REQUIRES esp_timer bt
                       PRIV_REQUIRES nvs_flash soc esp_pm esp_phy mbedtls driver vfs)

if(CONFIG_BT_ENABLED)
    if(CONFIG_BT_NIMBLE_MESH)
        set_source_files_properties("nimble/host/mesh/src/net.c"
            PROPERTIES COMPILE_FLAGS -Wno-type-limits)
    endif()

    target_compile_options(${COMPONENT_LIB} PRIVATE
                        -DCONFIG_BT_NIMBLE_ENABLED=1
                        -Wno-unused-but-set-variable
                        -Wno-unused-variable
                        -Wno-implicit-fallthrough
                        -Wno-format)
endif()
